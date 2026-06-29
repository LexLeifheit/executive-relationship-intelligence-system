from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import mean
from typing import Iterable


DATE_FORMATS = ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%m/%d/%Y")


@dataclass
class Relationship:
    name: str
    organization: str
    roles: list[str]
    purpose: list[str]
    influence: int | None
    health: int | None
    last_contact: date | None
    next_action: str
    follow_up_date: date | None
    next_conversation: str
    notes: str
    objective: str
    grade: str

    @property
    def priority_score(self) -> float:
        influence = self.influence or 0
        health_gap = 5 - (self.health or 3)
        grade_weight = {"A": 3, "B": 2, "C": 1}.get(self.grade.upper(), 1)
        follow_up_weight = 2 if self.follow_up_date and self.follow_up_date <= date.today() else 0
        return influence * 2 + health_gap + grade_weight + follow_up_weight


def parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            continue
    return None


def parse_int(value: str) -> int | None:
    value = value.strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def split_tags(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def load_relationships(path: Path) -> list[Relationship]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        return [
            Relationship(
                name=row.get("Name", "").strip(),
                organization=row.get("Organization", "").strip(),
                roles=split_tags(row.get("Relationship Roles", "")),
                purpose=split_tags(row.get("Relationship Purpose", "")),
                influence=parse_int(row.get("Influence", "")),
                health=parse_int(row.get("Health", "")),
                last_contact=parse_date(row.get("Last Contact", "")),
                next_action=row.get("Next Action", "").strip(),
                follow_up_date=parse_date(row.get("Follow-up Date", "")),
                next_conversation=row.get("Next Conversation", "").strip(),
                notes=row.get("Notes", "").strip(),
                objective=row.get("12-Month Objective", "").strip(),
                grade=row.get("Grade", "").strip(),
            )
            for row in reader
            if row.get("Name", "").strip()
        ]


def due_items(relationships: Iterable[Relationship]) -> list[Relationship]:
    today = date.today()
    return sorted(
        [item for item in relationships if item.follow_up_date and item.follow_up_date <= today],
        key=lambda item: (item.follow_up_date or today, item.grade, -item.priority_score),
    )


def stale_items(relationships: Iterable[Relationship], days: int) -> list[Relationship]:
    today = date.today()
    stale = []
    for item in relationships:
        if not item.last_contact:
            stale.append(item)
            continue
        if (today - item.last_contact).days >= days:
            stale.append(item)
    return sorted(stale, key=lambda item: (-item.priority_score, item.last_contact or date.min))


def format_date(value: date | None) -> str:
    return value.isoformat() if value else "unknown"


def markdown_cell(value: str) -> str:
    return (value or "n/a").replace("|", "\\|").replace("\n", " ").strip() or "n/a"


def sentence(value: str) -> str:
    return value.strip() if value.strip() else "n/a"


def this_week_items(relationships: Iterable[Relationship], run_date: date, days: int = 14) -> list[Relationship]:
    end_date = run_date + timedelta(days=days)
    return sorted(
        [
            item
            for item in relationships
            if item.follow_up_date and run_date <= item.follow_up_date <= end_date
        ],
        key=lambda item: (item.follow_up_date or end_date, -item.priority_score, item.name),
    )


def at_risk_items(relationships: Iterable[Relationship]) -> list[Relationship]:
    return sorted(
        [
            item
            for item in relationships
            if (item.influence or 0) >= 4 and (item.health or 0) <= 3
        ],
        key=lambda item: (
            item.health if item.health is not None else 99,
            -(item.influence or 0),
            item.follow_up_date or date.max,
            item.name,
        ),
    )


def fieldwave_pipeline_items(relationships: Iterable[Relationship]) -> list[Relationship]:
    return sorted(
        [item for item in relationships if any(role.lower() == "fieldwave" for role in item.roles)],
        key=lambda item: (item.last_contact is not None, item.last_contact or date.min, item.name),
        reverse=True,
    )


def write_weekly_report(relationships: list[Relationship], output: Path, run_date: date | None = None) -> None:
    run_date = run_date or date.today()
    upcoming = this_week_items(relationships, run_date)
    risk_items = at_risk_items(relationships)
    pipeline = fieldwave_pipeline_items(relationships)

    lines = [
        "# Weekly Relationship Intelligence Report",
        "",
        f"Generated: {run_date.isoformat()}",
        f"Window: {run_date.isoformat()} through {(run_date + timedelta(days=14)).isoformat()}",
        "",
        "## This Week",
        "",
    ]

    if upcoming:
        for item in upcoming:
            context = f"{item.name} ({item.organization or 'no organization'})"
            action = f" - {item.next_action}" if item.next_action else ""
            conversation = f" Next conversation: {item.next_conversation}" if item.next_conversation else ""
            lines.append(f"- {format_date(item.follow_up_date)}: {context}{action}.{conversation}".rstrip())
    else:
        lines.append("- No follow-ups are scheduled in the next 14 days.")

    lines.extend(["", "## At Risk Relationships", ""])
    if risk_items:
        for item in risk_items:
            lines.extend(
                [
                    f"### {item.name} ({item.organization or 'no organization'})",
                    "",
                    f"- Influence: {item.influence or 'n/a'}",
                    f"- Health: {item.health or 'n/a'}",
                    f"- Last contact: {format_date(item.last_contact)}",
                    f"- Follow-up date: {format_date(item.follow_up_date)}",
                    f"- Next conversation: {sentence(item.next_conversation)}",
                    f"- Notes: {sentence(item.notes)}",
                    f"- 12-month objective: {sentence(item.objective)}",
                    "",
                ]
            )
    else:
        lines.append("- No relationships currently meet the at-risk criteria.")

    lines.extend(
        [
            "",
            "## FIELDWAVE Pipeline",
            "",
            "| Name | Organization | Relationship Purpose | Last Contact | Follow-up Date | Next Action |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    if pipeline:
        for item in pipeline:
            lines.append(
                "| "
                + " | ".join(
                    [
                        markdown_cell(item.name),
                        markdown_cell(item.organization),
                        markdown_cell(", ".join(item.purpose)),
                        markdown_cell(format_date(item.last_contact)),
                        markdown_cell(format_date(item.follow_up_date)),
                        markdown_cell(item.next_action),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| n/a | n/a | n/a | n/a | n/a | n/a |")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown_report(relationships: list[Relationship], output: Path, stale_days: int) -> None:
    due = due_items(relationships)
    stale = stale_items(relationships, stale_days)
    role_counts = Counter(role for item in relationships for role in item.roles)
    grade_counts = Counter(item.grade or "Ungraded" for item in relationships)
    health_values = [item.health for item in relationships if item.health is not None]
    influence_values = [item.influence for item in relationships if item.influence is not None]

    lines = [
        "# Relationship Intelligence Report",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Portfolio",
        "",
        f"- Relationships: {len(relationships)}",
        f"- Average influence: {mean(influence_values):.1f}" if influence_values else "- Average influence: n/a",
        f"- Average health: {mean(health_values):.1f}" if health_values else "- Average health: n/a",
        f"- Grades: {', '.join(f'{grade} {count}' for grade, count in sorted(grade_counts.items()))}",
        "",
        "## Follow-ups Due",
        "",
    ]

    if due:
        lines.extend(
            f"- {item.name} ({item.organization or 'no organization'}): due {format_date(item.follow_up_date)}"
            + (f" - {item.next_action}" if item.next_action else "")
            for item in due
        )
    else:
        lines.append("- No follow-ups are currently due.")

    lines.extend(["", "## Stale Or At-Risk Relationships", ""])
    lines.extend(
        f"- {item.name} ({item.organization or 'no organization'}): last contact {format_date(item.last_contact)}, "
        f"health {item.health or 'n/a'}, influence {item.influence or 'n/a'}"
        for item in stale[:15]
    )

    lines.extend(["", "## Top Roles", ""])
    if role_counts:
        lines.extend(f"- {role}: {count}" for role, count in role_counts.most_common(10))
    else:
        lines.append("- No roles found.")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an Executive Relationship Intelligence CSV export.")
    parser.add_argument("csv_path", type=Path, help="Path to a Notion CSV export or compatible relationship CSV.")
    parser.add_argument("--output", type=Path, default=Path("reports/relationship-report.md"))
    parser.add_argument("--report", choices=("weekly", "portfolio"), default="weekly")
    parser.add_argument("--run-date", type=parse_date, help="Report run date. Defaults to today.")
    parser.add_argument("--stale-days", type=int, default=60)
    args = parser.parse_args()

    relationships = load_relationships(args.csv_path)
    if args.report == "weekly":
        write_weekly_report(relationships, args.output, args.run_date)
    else:
        write_markdown_report(relationships, args.output, args.stale_days)
    print(f"Wrote {args.output} for {len(relationships)} relationships.")


if __name__ == "__main__":
    main()
