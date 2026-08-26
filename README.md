# Executive Relationship Intelligence System

A private-first, AI-assisted workflow for tracking high-value relationships,
prioritizing follow-up, and turning relationship notes into a weekly executive
brief.

I built this as a minimal public demonstration of how I use AI for
judgment-heavy operating work: structuring messy relationship context,
protecting private data, and creating a repeatable briefing process that could
support a principal, policy leader, or executive team.

The public repository contains only sanitized sample data and reusable
documentation. Private relationship exports and generated reports stay local.

## Portfolio Framing

This project demonstrates skills that are relevant to policy, strategy, and
chief-of-staff roles:

- Building lightweight operating systems for ambiguous work.
- Translating private context into structured decision support.
- Maintaining stakeholder and relationship discipline.
- Using AI assistance while preserving human judgment and confidentiality.
- Creating documentation that another leader or team could adapt.

## What It Does

- Defines a practical relationship intelligence schema.
- Treats Notion as the private source of truth for relationship records.
- Supports ChatGPT/Codex-assisted updates to structured Notion fields and notes.
- Supports Notion CSV exports for local reporting.
- Keeps private relationship data out of GitHub.
- Generates a local markdown report with overdue follow-ups, stale
  relationships, at-risk relationships, and FIELDWAVE pipeline visibility.
- Documents the review cadence and scoring model so the system can be adapted
  for others.

## Public Demo

- [Public Case Study](docs/public-case-study.md)
- [AI-Assisted Workflow](docs/ai-assisted-workflow.md)
- [Sample Weekly Brief](docs/sample-weekly-brief.md)

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

Use a private Notion export or synced local cache:

```bash
cp /path/to/notion-export.csv data/private/relationships.csv
scripts/run_local_report.sh
```

The generated report will appear in `reports/`.

In the current operating model, Notion remains the source of truth. ChatGPT or
Codex can be used as a private update layer: the user describes a relationship
touchpoint in natural language, the assistant updates the matching Notion record
with structured fields and concise notes, and the local CSV/report workflow is
refreshed from that private source.

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

This is especially important because the project is meant to demonstrate the
workflow, not disclose the underlying relationship intelligence.

Relationship notes should follow a trust-preserving standard: store only what is
useful for respectful follow-up, avoid speculation or unnecessary sensitive
detail, and keep write actions explicit and reviewable.

## Documentation

- [System Design](docs/system-design.md)
- [Notion Setup](docs/notion-setup.md)
- [Operating Playbook](docs/operating-playbook.md)
- [Public Case Study](docs/public-case-study.md)
- [AI-Assisted Workflow](docs/ai-assisted-workflow.md)
- [Sample Weekly Brief](docs/sample-weekly-brief.md)

## Project Status

Version `0.1.0` is a lightweight documented foundation:

- schema captured from the existing Notion database
- sample data included
- local CSV reporting supported
- privacy guardrails in place

Future additions could include a first-class Notion sync command, calendar
reminders, contact freshness alerts, AI-assisted next-action drafting, and a
small browser dashboard.
