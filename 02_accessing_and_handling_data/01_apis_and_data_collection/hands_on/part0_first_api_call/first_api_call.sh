#!/usr/bin/env bash
# Practical, part 0 (slide 22): call a web API from the terminal and pretty-print the JSON with jq.
curl -s "https://api.open-meteo.com/v1/forecast?latitude=52&longitude=0&current=temperature_2m" | jq
