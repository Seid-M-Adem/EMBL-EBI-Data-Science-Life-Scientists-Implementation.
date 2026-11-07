"""Tests for dsls.ebi_api. Offline by default; `pytest -m network` runs the live smoke test."""

from __future__ import annotations

import json

import pytest
import requests

from dsls.ebi_api import (
    APIError,
    EBIClient,
    Response,
    build_url,
    chembl,
    json_next,
    link_header_next,
    uniprot,
)


class FakeResponse:
    def __init__(self, status=200, body=b"{}", headers=None, url=None):
        self.status_code = status
        self.content = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.headers = headers or {}
        self.url = url
        self.text = self.content.decode()


class FakeSession:
    """Plays back scripted responses (or raises scripted exceptions) and records requested URLs."""

    def __init__(self, *script):
        self.script = list(script)
        self.calls: list[str] = []
        self.headers: dict[str, str] = {}

    def get(self, url, headers=None, timeout=None):
        self.calls.append(url)
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def make_client(session, tmp_path=None, **kwargs):
    sleeps: list[float] = []
    client = EBIClient(
        "https://api.example.org",
        "test",
        session=session,
        sleep=sleeps.append,
        cache_dir=tmp_path if tmp_path else False,
        **kwargs,
    )
    return client, sleeps


# ----------------------------------------------------------------------------- URLs
def test_build_url_sorts_params_and_drops_none():
    url = build_url("https://x.org/api", "items", {"b": 2, "a": "x y", "skip": None})
    assert url == "https://x.org/api/items?a=x+y&b=2"


def test_build_url_passes_absolute_urls_through():
    assert build_url("https://x.org", "https://other.org/p?q=1", {"r": 2}) == "https://other.org/p?q=1&r=2"


# ----------------------------------------------------------------------------- retries
def test_retries_on_503_then_succeeds():
    session = FakeSession(FakeResponse(503), FakeResponse(503), FakeResponse(200, {"ok": True}))
    client, sleeps = make_client(session, backoff=1.0)
    assert client.get_json("thing") == {"ok": True}
    assert len(session.calls) == 3
    assert len(sleeps) == 2 and 1.0 <= sleeps[0] <= 2.0 and 2.0 <= sleeps[1] <= 3.0  # exponential + jitter


def test_retry_after_header_is_honoured():
    session = FakeSession(FakeResponse(429, headers={"Retry-After": "7"}), FakeResponse(200, {}))
    client, sleeps = make_client(session, backoff=0.0)
    client.get("thing")
    assert sleeps == [7.0]


def test_connection_errors_are_retried():
    session = FakeSession(requests.ConnectionError("reset"), FakeResponse(200, {"n": 1}))
    client, _ = make_client(session)
    assert client.get_json("thing") == {"n": 1}


def test_gives_up_after_max_retries():
    session = FakeSession(*[FakeResponse(500) for _ in range(3)])
    client, sleeps = make_client(session, max_retries=2)
    with pytest.raises(APIError, match="after 3 attempts"):
        client.get("thing")
    assert len(sleeps) == 2


def test_client_errors_fail_fast_without_retry():
    session = FakeSession(FakeResponse(400, b"bad query"))
    client, sleeps = make_client(session)
    with pytest.raises(APIError) as err:
        client.get("thing")
    assert err.value.status == 400 and "bad query" in str(err.value)
    assert sleeps == [] and len(session.calls) == 1


# ----------------------------------------------------------------------------- caching
def test_cache_hit_skips_network_and_keeps_provenance(tmp_path):
    headers = {"Content-Type": "application/json", "X-UniProt-Release": "2026_04"}
    session = FakeSession(FakeResponse(200, {"v": 1}, headers=headers))
    client, _ = make_client(session, tmp_path)
    first = client.get("thing", {"q": 1})
    second = client.get("thing", {"q": 1})
    assert not first.from_cache and second.from_cache
    assert second.json() == {"v": 1} and len(session.calls) == 1
    meta = json.loads(next(tmp_path.glob("*.meta.json")).read_text())
    assert meta["provenance"]["x-uniprot-release"] == "2026_04"
    assert meta["request_url"] == "https://api.example.org/thing?q=1"


def test_refresh_bypasses_cache(tmp_path):
    session = FakeSession(FakeResponse(200, {"v": 1}), FakeResponse(200, {"v": 2}))
    client, _ = make_client(session, tmp_path)
    client.get("thing")
    assert client.get("thing", refresh=True).json() == {"v": 2}


def test_errors_are_not_cached(tmp_path):
    session = FakeSession(FakeResponse(404, b"nope"), FakeResponse(200, {"v": 1}))
    client, _ = make_client(session, tmp_path)
    with pytest.raises(APIError):
        client.get("thing")
    assert client.get_json("thing") == {"v": 1}


def test_different_accept_types_are_cached_separately(tmp_path):
    session = FakeSession(FakeResponse(200, b"a\tb"), FakeResponse(200, {"a": 1}))
    client, _ = make_client(session, tmp_path)
    assert client.get("t", accept="text/tab-separated-values").text == "a\tb"
    assert client.get_json("t") == {"a": 1}


# ----------------------------------------------------------------------------- pagination
def test_link_header_pagination_uniprot_style():
    nxt = '<https://rest.uniprot.org/uniprotkb/search?cursor=abc&size=2>; rel="next"'
    session = FakeSession(
        FakeResponse(200, {"results": [1, 2]}, headers={"Link": nxt}),
        FakeResponse(200, {"results": [3]}),
    )
    client = uniprot(session=session, cache_dir=False, sleep=lambda s: None)
    assert list(client.paginate_items("uniprotkb/search", {"query": "x", "size": 2})) == [1, 2, 3]
    assert session.calls[1] == "https://rest.uniprot.org/uniprotkb/search?cursor=abc&size=2"


def test_link_header_with_commas_in_url():
    """Regression: UniProt next links contain commas (fields=a,b,c); the header must not be split on them."""
    nxt = "https://rest.uniprot.org/uniprotkb/search?fields=accession,length,ft_motif&cursor=x1&size=100"
    page = Response(url="u", status=200, headers={"link": f'<{nxt}>; rel="next"'}, content=b"{}")
    assert link_header_next(page) == nxt


def test_json_next_pagination_chembl_style():
    p1 = {"activities": [{"id": 1}], "page_meta": {"next": "/chembl/api/data/activity.json?offset=1"}}
    p2 = {"activities": [{"id": 2}], "page_meta": {"next": None}}
    session = FakeSession(FakeResponse(200, p1), FakeResponse(200, p2))
    client = chembl("activities", session=session, cache_dir=False, sleep=lambda s: None)
    ids = [a["id"] for a in client.paginate_items("chembl/api/data/activity.json", {"limit": 1})]
    assert ids == [1, 2]
    assert session.calls[1] == "https://www.ebi.ac.uk/chembl/api/data/activity.json?offset=1"


def test_max_pages_stops_early():
    page = FakeResponse(200, {"results": [0]}, headers={"Link": '<https://x.org/next>; rel="next"'})
    session = FakeSession(page, page, page)
    client = uniprot(session=session, cache_dir=False)
    assert len(list(client.paginate("s", max_pages=2))) == 2


def test_strategies_return_none_at_the_end():
    last = Response(url="u", status=200, headers={}, content=b'{"page_meta": {"next": null}}')
    assert link_header_next(last) is None
    assert json_next("page_meta", "next")(last) is None
    assert json_next("missing", "next")(last) is None


def test_paginate_without_strategy_raises():
    client, _ = make_client(FakeSession())
    with pytest.raises(ValueError, match="pagination strategy"):
        next(client.paginate("x"))


# ----------------------------------------------------------------------------- live
@pytest.mark.network
def test_live_uniprot_smoke(tmp_path):
    client = uniprot(cache_dir=tmp_path)
    page = client.get("uniprotkb/search", {"query": "accession:P69905", "fields": "accession,gene_names"})
    assert page.json()["results"][0]["primaryAccession"] == "P69905"  # haemoglobin alpha
    assert "x-uniprot-release" in page.headers
