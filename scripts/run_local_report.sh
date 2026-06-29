#!/usr/bin/env bash
set -euo pipefail

CSV_PATH="${1:-data/private/relationships.csv}"
python3 -m src.eris.analyze "$CSV_PATH" --report weekly --output reports/weekly-relationship-report.md
