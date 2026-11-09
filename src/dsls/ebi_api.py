"""A small, dependable client for EMBL-EBI REST APIs.

One class, :class:`EBIClient`, adds three things the course's ad-hoc ``requests.get`` calls lack:

* **Retries** - connection errors and HTTP 429/5xx are retried with exponential backoff and jitter,
  honouring the server's ``Retry-After`` header. Other 4xx errors fail immediately with a clear message.
* **Pagination** - :meth:`EBIClient.paginate` walks every page of a result set. EBI services paginate in
  different ways, so the strategy is a small function; ready-made ones cover UniProt (``Link`` header),
  ChEMBL (``page_meta.next``) and MGnify / JSON:API (``links.next``).
* **Caching** - successful responses are stored under ``data/raw/api_cache/<service>/`` together with a
  provenance record (URL, fetch time, data release). Re-running an analysis is instant, works offline,
  and the raw data behind every result is kept, in line with FAIR practice.

Example::

    from dsls.ebi_api import uniprot

    client = uniprot()
    for entry in client.paginate_items("uniprotkb/search",
                                       {"query": "family:aquaporin AND reviewed:true", "size": 500}):
        print(entry["primaryAccession"])
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import time
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urljoin

import requests
from requests.structures import CaseInsensitiveDict

__all__ = [
    "APIError",
    "EBIClient",
    "Response",
    "chembl",
    "ena_portal",
    "json_next",
    "link_header_next",
    "mgnify",
    "reactome",
    "uniprot",
]

USER_AGENT = (
    "dsls-portfolio/0.1 "
    "(+https://github.com/Seid-M-Adem/EMBL-EBI-Data-Science-Life-Scientists-Implementation)"
)
_LINK_NEXT = re.compile(r'<([^>]*)>\s*;\s*rel="?next"?')
RETRY_STATUS = frozenset({429, 500, 502, 503, 504})
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CACHE_ROOT = REPO_ROOT / "data" / "raw" / "api_cache"
# Response headers worth keeping in the provenance record (data release / version information).
PROVENANCE_HEADERS = ("content-type", "x-uniprot-release", "x-uniprot-release-date", "x-total-results")


class APIError(RuntimeError):
    """A request that failed permanently (non-retryable status, or retries exhausted)."""

    def __init__(self, message: str, *, url: str, status: int | None = None):
        super().__init__(message)
        self.url = url
        self.status = status


@dataclass(frozen=True)
class Response:
    """The parts of an HTTP response an analysis needs; identical whether live or from the cache."""

    url: str
    status: int
    headers: Mapping[str, str]  # case-insensitive, like real HTTP headers
    content: bytes
    from_cache: bool = False
    fetched_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat(timespec="seconds"))

    @property
    def text(self) -> str:
        return self.content.decode("utf-8")

    def json(self) -> Any:
        return json.loads(self.content)


def build_url(base_url: str, path: str, params: dict[str, Any] | None = None) -> str:
    """Join ``base_url`` and ``path`` (absolute URLs pass through) and append sorted query parameters."""
    url = (
        path
        if path.startswith(("http://", "https://"))
        else urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    )
    if params:
        clean = {k: v for k, v in sorted(params.items()) if v is not None}
        url += ("&" if "?" in url else "?") + urlencode(clean, doseq=True)
    return url


class EBIClient:
    """HTTP client for one EBI service, with retries, pagination and an on-disk cache.

    Args:
        base_url: Service root, e.g. ``https://rest.uniprot.org``.
        name: Short service name, used for the cache sub-folder.
        cache_dir: Where to cache responses. ``None`` uses ``data/raw/api_cache/<name>``;
            ``False`` disables caching.
        max_retries: Retries after the first attempt for retryable failures.
        backoff: Base delay in seconds; attempt *n* waits ``backoff * 2**n`` (+ jitter, max 60 s).
        timeout: Per-request timeout in seconds.
        session: Optional ``requests.Session`` (tests inject a fake one).
        sleep: Function used to wait between retries (tests inject a no-op).
    """

    def __init__(
        self,
        base_url: str,
        name: str,
        *,
        cache_dir: Path | str | None | bool = None,
        max_retries: int = 5,
        backoff: float = 1.0,
        timeout: float = 60.0,
        session: requests.Session | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        self.base_url = base_url
        self.name = name
        if cache_dir is False:
            self.cache_dir: Path | None = None
        else:
            self.cache_dir = Path(cache_dir) if cache_dir else DEFAULT_CACHE_ROOT / name
        self.max_retries = max_retries
        self.backoff = backoff
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.setdefault("User-Agent", USER_AGENT)
        self._sleep = sleep

    # ---------------------------------------------------------------- requests
    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        *,
        accept: str = "application/json",
        refresh: bool = False,
    ) -> Response:
        """GET ``path`` (relative to ``base_url``, or an absolute URL), using the cache unless ``refresh``."""
        url = build_url(self.base_url, path, params)
        if not refresh and (cached := self._cache_read(url, accept)):
            return cached
        response = self._fetch(url, accept)
        self._cache_write(url, accept, response)
        return response

    def get_json(self, path: str, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        return self.get(path, params, **kwargs).json()

    def post(
        self,
        path: str,
        body: str,
        params: dict[str, Any] | None = None,
        *,
        content_type: str = "text/plain",
        accept: str = "application/json",
        refresh: bool = False,
    ) -> Response:
        """POST ``body`` to ``path``, for read-only analysis services that take their input in the request body.

        Cached like :meth:`get`; the cache key includes a hash of the body, so a different input is a different
        entry. Only use it for requests that don't change anything on the server.
        """
        url = build_url(self.base_url, path, params)
        digest = hashlib.sha256(f"{content_type}\n{body}".encode()).hexdigest()[:16]
        key = f"POST {url} body={digest}"
        if not refresh and (cached := self._cache_read(key, accept)):
            return cached
        response = self._fetch(url, accept, data=body.encode(), content_type=content_type)
        self._cache_write(key, accept, response)
        return response

    def _fetch(
        self, url: str, accept: str, data: bytes | None = None, content_type: str | None = None
    ) -> Response:
        last_error = ""
        for attempt in range(self.max_retries + 1):
            retry_after: float | None = None
            try:
                if data is None:
                    r = self.session.get(url, headers={"Accept": accept}, timeout=self.timeout)
                else:
                    headers = {"Accept": accept, "Content-Type": content_type or "text/plain"}
                    r = self.session.post(url, data=data, headers=headers, timeout=self.timeout)
            except requests.RequestException as exc:  # connection reset, DNS, timeout, ...
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                if r.status_code < 400:
                    headers = CaseInsensitiveDict({k.lower(): v for k, v in r.headers.items()})
                    return Response(
                        url=getattr(r, "url", None) or url,
                        status=r.status_code,
                        headers=headers,
                        content=r.content,
                    )
                if r.status_code not in RETRY_STATUS:
                    raise APIError(
                        f"HTTP {r.status_code} for {url}: {r.text[:300]}", url=url, status=r.status_code
                    )
                last_error = f"HTTP {r.status_code}"
                retry_after = _parse_retry_after(r.headers.get("Retry-After"))
            if attempt < self.max_retries:
                delay = retry_after if retry_after is not None else self.backoff * 2**attempt
                self._sleep(min(delay + random.uniform(0, self.backoff), 60.0))
        raise APIError(f"Giving up on {url} after {self.max_retries + 1} attempts ({last_error})", url=url)

    # ---------------------------------------------------------------- pagination
    def paginate(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        *,
        next_page: Callable[[Response], str | None] | None = None,
        max_pages: int | None = None,
        **kwargs: Any,
    ) -> Iterator[Response]:
        """Yield every page of a result set, following ``next_page`` until it returns ``None``.

        ``next_page`` receives a page and returns the next page's URL (absolute, or relative to
        ``base_url``). The default comes from the service factory (``uniprot()``, ``chembl()``, ...).
        """
        strategy = next_page or getattr(self, "default_next_page", None)
        if strategy is None:
            raise ValueError("No pagination strategy: pass next_page=link_header_next / json_next(...)")
        page = self.get(path, params, **kwargs)
        pages = 1
        yield page
        while (nxt := strategy(page)) and (max_pages is None or pages < max_pages):
            page = self.get(nxt, **kwargs)
            pages += 1
            yield page

    def paginate_items(
        self, path: str, params: dict[str, Any] | None = None, *, items_key: str | None = None, **kwargs: Any
    ) -> Iterator[Any]:
        """Like :meth:`paginate`, but yield the individual records from each page's JSON."""
        key = items_key or getattr(self, "default_items_key", None)
        if key is None:
            raise ValueError("Pass items_key=... (the JSON field that holds the records)")
        for page in self.paginate(path, params, **kwargs):
            yield from page.json()[key]

    # ---------------------------------------------------------------- cache
    def _cache_paths(self, url: str, accept: str) -> tuple[Path, Path] | None:
        if self.cache_dir is None:
            return None
        key = hashlib.sha256(f"{accept} {url}".encode()).hexdigest()[:24]
        return self.cache_dir / f"{key}.body", self.cache_dir / f"{key}.meta.json"

    def _cache_read(self, url: str, accept: str) -> Response | None:
        paths = self._cache_paths(url, accept)
        if not paths or not paths[0].exists() or not paths[1].exists():
            return None
        meta = json.loads(paths[1].read_text())
        return Response(
            url=meta["url"],
            status=meta["status"],
            headers=CaseInsensitiveDict(meta["headers"]),
            content=paths[0].read_bytes(),
            from_cache=True,
            fetched_at=meta["fetched_at"],
        )

    def _cache_write(self, url: str, accept: str, response: Response) -> None:
        paths = self._cache_paths(url, accept)
        if not paths:
            return
        paths[0].parent.mkdir(parents=True, exist_ok=True)
        paths[0].write_bytes(response.content)
        meta = {
            "request_url": url,
            "url": response.url,
            "accept": accept,
            "status": response.status,
            "fetched_at": response.fetched_at,
            "headers": dict(response.headers),
            "provenance": {h: response.headers[h] for h in PROVENANCE_HEADERS if h in response.headers},
        }
        paths[1].write_text(json.dumps(meta, indent=2))


# -------------------------------------------------------------------- pagination strategies
def link_header_next(page: Response) -> str | None:
    """Next-page URL from an RFC 8288 ``Link: <url>; rel="next"`` header (UniProt REST).

    Matched with a pattern rather than split on commas: the URL itself often contains commas
    (e.g. ``fields=accession,length``).
    """
    match = _LINK_NEXT.search(page.headers.get("link", ""))
    return match.group(1) if match else None


def json_next(*keys: str) -> Callable[[Response], str | None]:
    """Strategy that reads the next-page URL from a nested JSON field, e.g. ``json_next("page_meta", "next")``."""

    def strategy(page: Response) -> str | None:
        node: Any = page.json()
        for key in keys:
            if not isinstance(node, dict):
                return None
            node = node.get(key)
        return node or None

    strategy.__name__ = "json_next_" + "_".join(keys)
    return strategy


# -------------------------------------------------------------------- service factories
def _client(
    base_url: str,
    name: str,
    next_page: Callable[[Response], str | None] | None,
    items_key: str | None,
    **kwargs: Any,
) -> EBIClient:
    client = EBIClient(base_url, name, **kwargs)
    client.default_next_page = next_page  # type: ignore[attr-defined]
    client.default_items_key = items_key  # type: ignore[attr-defined]
    return client


def uniprot(**kwargs: Any) -> EBIClient:
    """UniProt REST API (https://rest.uniprot.org). Records are under ``results``."""
    return _client("https://rest.uniprot.org", "uniprot", link_header_next, "results", **kwargs)


def chembl(items_key: str | None = None, **kwargs: Any) -> EBIClient:
    """ChEMBL web services (https://www.ebi.ac.uk/chembl/api/data). Records key depends on the
    endpoint (``activities``, ``molecules``, ...), so pass ``items_key`` here or per call."""
    return _client("https://www.ebi.ac.uk", "chembl", json_next("page_meta", "next"), items_key, **kwargs)


def mgnify(**kwargs: Any) -> EBIClient:
    """MGnify API (JSON:API style, https://www.ebi.ac.uk/metagenomics/api/v1). Records under ``data``."""
    return _client(
        "https://www.ebi.ac.uk/metagenomics/api/v1", "mgnify", json_next("links", "next"), "data", **kwargs
    )


def ena_portal(**kwargs: Any) -> EBIClient:
    """ENA Portal API (https://www.ebi.ac.uk/ena/portal/api). It returns all rows in one response
    when ``limit=0``, so no pagination strategy is needed; use ``accept="text/tab-separated-values"``."""
    return _client("https://www.ebi.ac.uk/ena/portal/api", "ena", None, None, **kwargs)


def reactome(**kwargs: Any) -> EBIClient:
    """Reactome Analysis Service (https://reactome.org/AnalysisService): pathway over-representation analysis.

    Post a newline-separated list of identifiers (gene symbols, UniProt accessions) with :meth:`EBIClient.post` to
    ``identifiers/projection``; results are under ``pathways``.
    """
    return _client("https://reactome.org/AnalysisService", "reactome", None, "pathways", **kwargs)


def _parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(float(value), 0.0)
    except ValueError:  # HTTP-date form; fall back to exponential backoff
        return None
