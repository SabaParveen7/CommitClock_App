"""
Generates data/commits.json — 160 commit entries spread across
2026-06-12 .. 2026-07-11 (30 days).

Run again any time you want to regenerate the schedule, e.g. after
swapping in your real MedSim commit messages.

NOTE: the commit "message" field below is a generic placeholder
("Commit #N: ..."). Replace these with your actual MedSim commit
messages before using this for the real campaign — the schedule
engine only cares about date/time, the message is just what's shown
on the alarm screen.
"""
import json
from datetime import date, timedelta

START = date(2026, 6, 12)
DAYS = 30
TOTAL_COMMITS = 160

BASE_SLOTS = ["09:00", "11:30", "14:00", "16:30", "19:00"]   # 5/day baseline
EXTRA_SLOT = "21:00"                                          # 6th slot on bonus days

PLACEHOLDER_VERBS = [
    "Add", "Refactor", "Fix", "Update", "Implement", "Improve",
    "Document", "Clean up", "Optimize", "Wire up"
]
PLACEHOLDER_AREAS = [
    "data model", "UI layer", "test suite", "README", "API client",
    "simulation core", "config", "logging", "error handling", "build script"
]

def build_schedule():
    entries = []
    commit_id = 1
    days = [START + timedelta(days=i) for i in range(DAYS)]

    # First 10 days get 6 slots, remaining 20 days get 5 slots
    # 10*6 + 20*5 = 60 + 100 = 160
    for i, day in enumerate(days):
        slots = BASE_SLOTS + ([EXTRA_SLOT] if i < 10 else [])
        for t in slots:
            verb = PLACEHOLDER_VERBS[commit_id % len(PLACEHOLDER_VERBS)]
            area = PLACEHOLDER_AREAS[commit_id % len(PLACEHOLDER_AREAS)]
            entries.append({
                "id": commit_id,
                "date": day.isoformat(),
                "time": t,
                "message": f"Commit #{commit_id}: {verb} {area}",
                "status": "pending"   # pending | done | missed
            })
            commit_id += 1

    assert len(entries) == TOTAL_COMMITS, f"Expected {TOTAL_COMMITS}, got {len(entries)}"
    return entries

if __name__ == "__main__":
    schedule = build_schedule()
    with open("data/commits.json", "w") as f:
        json.dump(schedule, f, indent=2)
    print(f"Wrote {len(schedule)} entries to data/commits.json")
