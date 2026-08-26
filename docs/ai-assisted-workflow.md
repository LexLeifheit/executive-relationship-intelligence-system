# AI-Assisted Workflow

This project was built as an example of using AI to make private operational
work more structured, legible, and repeatable.

## Human Inputs

- Relationship judgment.
- Role and purpose tags.
- Health and influence scoring.
- Notes from real conversations.
- Decisions about what should remain private.

## AI-Assisted Steps

- Translate a Notion export into a documented project structure.
- Convert an implicit relationship-management practice into a clear schema.
- Convert natural-language relationship updates into structured Notion records.
- Generate a local report workflow from structured CSV data.
- Create reusable documentation and sample data.
- Add privacy guardrails so sensitive exports stay local.

## Review Loop

The workflow is designed for a weekly review:

1. Update Notion as the source of truth for new relationship context.
2. Export or sync the latest relationship data to the local private CSV.
3. Generate the private weekly brief.
4. Review near-term follow-ups.
5. Inspect at-risk high-influence relationships.
6. Update next actions, conversation notes, and objectives.
7. Keep public documentation sanitized.

## Conversational Update Loop

The prototype can also be used between weekly reviews:

1. The user captures a touchpoint in plain language.
2. The assistant identifies the matching Notion record or proposes a new one.
3. The assistant updates only the fields needed for the touchpoint: last contact,
   health, follow-up date, next action, next conversation, role or purpose tags,
   and concise notes.
4. The assistant verifies the changed record and keeps private details out of
   GitHub.

This loop is intended to behave like lightweight chief-of-staff support: it
preserves useful context, turns memory into follow-up discipline, and leaves
judgment with the human user.

## Trust-Preserving Notes

Relationship notes should be written as if the person could read them and find
them fair. Store enough context to be considerate and effective, but avoid
unnecessary detail about health, family, finances, conflict, or private plans.
Prefer factual observations and explicit next actions over speculation.

## Privacy Boundary

The repository demonstrates the method, not the private contents. Public files
show the schema and sample output. Private CSV exports and generated reports
are ignored locally and should not be pushed to GitHub.
