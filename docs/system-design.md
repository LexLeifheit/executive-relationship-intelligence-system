# System Design

The Executive Relationship Intelligence System is a lightweight relationship
operating system. It starts as a Notion database and can be repurposed as a
local, private analysis workflow for any executive, founder, operator, job
seeker, fundraiser, or civic leader who manages a high-trust network.

## Core Objects

The system currently centers on a single `Relationship` object. A relationship
represents a person and the context needed to maintain intentional contact:

- Identity: name and organization.
- Strategy: relationship roles, purpose, grade, and 12-month objective.
- Signal: influence, health, last contact, and notes.
- Action: next action, follow-up date, and next conversation.

## Operating Cadence

Weekly review:

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

The repository is designed so personal relationship data stays local. Raw
exports belong under `data/private/`, which is ignored by Git. Public examples
belong under `data/sample/` and should be sanitized.

## Repurposing Model

To adapt this system for another person or organization:

1. Copy the schema in `config/schema.yml`.
2. Create or export a compatible CSV.
3. Keep personal data in `data/private/`.
4. Run the report workflow.
5. Adjust roles, purpose tags, grade definitions, and review cadence for the
   new operating context.
