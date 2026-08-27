#!/usr/bin/env bash
set -euo pipefail

profile_url="${1:?Usage: ./examples/profile-export.sh <profile-url> [result-json]}"
result_json="${2:-output/result.json}"

python -m pip install -e '.[agent]'
douyin-ingest "$profile_url" --limit 0 --export docx --output "$result_json"
