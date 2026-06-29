# Notion Setup

Create a Notion database named `Relationship Intelligence` with the fields
listed in `config/schema.yml`.

Recommended views:

- `Weekly Review`: sorted by follow-up date, grade, and influence.
- `Strategic Map`: grouped by relationship role.
- `At Risk`: filtered to low health, stale contact, or overdue follow-up.
- `A List`: filtered to grade A.

Export instructions:

1. In Notion, open the database menu.
2. Choose export as CSV.
3. Save the CSV locally.
4. Place a copy at `data/private/relationships.csv`.
5. Run `scripts/run_local_report.sh`.

Do not commit personal exports to GitHub. Use `data/sample/relationships.csv`
when demonstrating the project.
