#!/usr/bin/env bash
# Asamblează site-ul publicabil în dist/:
#   - conținutul website/ ajunge la rădăcină (homepage direct pe domeniu)
#   - assets/ vine alături, iar căile relative se corectează corespunzător
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf dist
mkdir -p dist
cp -r website/* dist/
cp -r assets dist/assets

# structura publicată e plată: ../assets → assets (homepage), ../../assets → ../assets (pagini)
sed -i 's#\.\./assets/#assets/#g' dist/index.html
sed -i 's#\.\./\.\./assets/#../assets/#g' dist/pagini/*.html

echo "dist/ pregătit:"
find dist -maxdepth 1
