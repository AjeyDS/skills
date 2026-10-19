#!/usr/bin/env bash
# Zip each skill folder into dist/<name>.zip for upload to Claude.ai
# (Customize > Skills > Upload a skill). The zip holds the <name>/ folder.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
for dir in skills/*/*/; do
  name=$(basename "$dir")
  (cd "$(dirname "$dir")" && zip -qr "../../dist/$name.zip" "$name" -x '*.DS_Store' '*__pycache__*')
  echo "dist/$name.zip"
done
