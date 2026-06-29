from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
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
    parser.add_argument("--stale-days", type=int, default=60)
    args = parser.parse_args()

    relationships = load_relationships(args.csv_path)
    write_markdown_report(relationships, args.output, args.stale_days)
    print(f"Wrote {args.output} for {len(relationships)} relationships.")


if __name__ == "__main__":
    main()
