# System Design

The Executive Relationship Intelligence System is a lightweight relationship
operating system. It uses Notion as the private source of truth and can be
repurposed as a local, private analysis workflow for any executive, founder,
operator, job seeker, fundraiser, or civic leader who manages a high-trust
network.

## Core Objects

The system currently centers on a single `Relationship` object. A relationship
represents a person and the context needed to maintain intentional contact:

- Identity: name and organization.
- Strategy: relationship roles, purpose, grade, and 12-month objective.
- Signal: influence, health, last contact, and notes.
- Action: next action, follow-up date, and next conversation.

## Operating Cadence

Between reviews:

- Capture meaningful touchpoints in natural language.
- Update the matching Notion record with structured fields and concise notes.
- Prefer explicit follow-up dates and next actions when action is needed.
- Use no follow-up when the contact should simply refresh relationship context.

Weekly review:

- Refresh the local private CSV from Notion.
- Review follow-ups due now.
- Scan A-grade relationships with stale last-contact dates.
- Add next actions for relationships with strategic value but no active motion.

Monthly review:

- Regrade the portfolio.
- Update health scores for high-influence relationships.
- Review whether role tags still reflect current strategy.

Quarterly review:

- Rewrite 12-month objectives.
- Identify neglected relationship clusters.
- Archive relationships that no longer need active attention.

## Privacy Model

The repository is designed so personal relationship data stays private. Notion
holds the working database. Raw exports belong under `data/private/`, which is
ignored by Git. Generated reports belong under `reports/`, which is also ignored
by Git. Public examples belong under `data/sample/` and should be sanitized.

The system should minimize sensitive detail. Notes should be factual, useful for
respectful follow-up, and free of speculation. Health, family, job-search,
funding, and conflict-related context should be captured only when it supports a
legitimate relationship-maintenance purpose.

## Repurposing Model

To adapt this system for another person or organization:

1. Copy the schema in `config/schema.yml`.
2. Create a private Notion database using the schema.
3. Decide which AI assistant or workflow is allowed to update Notion.
4. Export or sync a compatible CSV into `data/private/` for local reporting.
5. Run the report workflow.
6. Adjust roles, purpose tags, grade definitions, and review cadence for the
   new operating context.
