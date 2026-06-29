# Executive Relationship Intelligence System

A private-first operating system for tracking high-value relationships,
prioritizing follow-up, and turning relationship notes into intentional action.

This project is built from a real Notion relationship database, but it is
structured so the personal data stays local and the repository can be reused by
other executives, operators, founders, fundraisers, job seekers, and civic
leaders.

## What It Does

- Defines a practical relationship intelligence schema.
- Supports Notion CSV exports.
- Keeps private relationship data out of GitHub.
- Generates a local markdown report with overdue follow-ups, stale
  relationships, at-risk relationships, and FIELDWAVE pipeline visibility.
- Documents the review cadence and scoring model so the system can be adapted
  for others.

## Repository Structure

```text
config/schema.yml              Field definitions and recommended views
data/sample/relationships.csv  Sanitized demo data
data/private/                  Local private exports, ignored by Git
docs/                          Setup, design, and operating playbook
reports/                       Local generated reports, ignored by Git
src/eris/analyze.py            CSV analyzer and report generator
scripts/run_local_report.sh    Convenience script for local reports
```

## Quick Start

Run the sample report:

```bash
python3 -m src.eris.analyze data/sample/relationships.csv --report weekly --output reports/sample-report.md
```

Use a private Notion export:

```bash
cp /path/to/notion-export.csv data/private/relationships.csv
scripts/run_local_report.sh
```

The generated report will appear in `reports/`.

The weekly report includes:

- `This Week`: relationships with follow-up dates in the next 14 days.
- `At Risk Relationships`: influence `>= 4` and health `<= 3`, with next
  conversation, notes, and 12-month objective.
- `FIELDWAVE Pipeline`: relationships tagged `FIELDWAVE`, including purpose,
  sorted by most recent last contact.

## Data Privacy

Personal relationship exports should not be committed. The `.gitignore` file
excludes `data/private/`, `reports/`, and exported ZIP files. Keep public demos
sanitized and place them in `data/sample/`.

## Documentation

- [System Design](docs/system-design.md)
- [Notion Setup](docs/notion-setup.md)
- [Operating Playbook](docs/operating-playbook.md)

## Project Status

Version `0.1.0` is a lightweight documented foundation:

- schema captured from the existing Notion database
- sample data included
- local CSV reporting supported
- privacy guardrails in place

Future additions could include calendar reminders, contact freshness alerts,
AI-assisted next-action drafting, and a small browser dashboard.
