# Notion Setup

Create a Notion database named `Relationship Intelligence` with the fields
listed in `config/schema.yml`. Treat this database as the private source of
truth for ERIS relationship records.

Recommended views:

- `Weekly Review`: sorted by follow-up date, grade, and influence.
- `Strategic Map`: grouped by relationship role.
- `At Risk`: filtered to low health, stale contact, or overdue follow-up.
- `A List`: filtered to grade A.

## ChatGPT/Codex-Assisted Updates

For daily use, the fastest update path is natural language:

1. Describe the relationship update in ChatGPT or Codex.
2. Confirm the intended person, date, health score, follow-up, and note.
3. Write the update to the matching Notion record.
4. Create a new Notion record only when no matching contact exists.
5. Keep notes concise, factual, and useful for respectful follow-up.

When name spellings or affiliations are ambiguous, prefer the database spelling
or verify against a reliable public source before changing the record.

## Local Reporting Export

Export or sync instructions:

1. In Notion, open the database menu.
2. Choose export as CSV.
3. Save the CSV locally.
4. Place a copy at `data/private/relationships.csv`.
5. Run `scripts/run_local_report.sh`.

Do not commit personal exports to GitHub. Use `data/sample/relationships.csv`
when demonstrating the project.

The local CSV is a private reporting artifact, not the source of truth. Refresh
it from Notion before generating a weekly report.

The default local report is designed for Monday morning review. It shows
follow-ups in the next 14 days, high-influence relationships with lower health,
and the opportunity pipeline sorted by last-contact date.
