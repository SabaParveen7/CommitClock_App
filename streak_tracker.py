"""
streak_tracker.py
------------------
Pure logic for streaks and the 30-day heatmap. No Kivy imports here on
purpose, so this module can be unit-tested or reused headlessly.

A "streak" = consecutive commits marked done, counting back from the
most recent commit whose scheduled time has already passed. Missing a
slot (status still "pending" after its scheduled time, or explicitly
"missed") breaks the streak.
"""
import json
import os
from datetime import datetime

MILESTONES = [5, 10, 20, 30, 50, 75, 100, 160]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
COMMITS_PATH = os.path.join(DATA_DIR, "commits.json")
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.json")


def load_commits():
    with open(COMMITS_PATH, "r") as f:
        return json.load(f)


def save_commits(commits):
    with open(COMMITS_PATH, "w") as f:
        json.dump(commits, f, indent=2)


def load_settings():
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)


def _scheduled_dt(entry):
    return datetime.strptime(f"{entry['date']} {entry['time']}", "%Y-%m-%d %H:%M")


def mark_done(commits, commit_id):
    """Mark a commit as done. Returns the updated list."""
    for e in commits:
        if e["id"] == commit_id:
            e["status"] = "done"
            break
    return commits


def mark_missed_if_overdue(commits, now=None):
    """
    Sweep the schedule: any 'pending' entry whose scheduled time is more
    than 1 minute in the past becomes 'missed'. Call this on app start
    and whenever the schedule screen is shown.
    """
    now = now or datetime.now()
    for e in commits:
        if e["status"] == "pending" and (now - _scheduled_dt(e)).total_seconds() > 60:
            e["status"] = "missed"
    return commits


def progress_counts(commits):
    done = sum(1 for e in commits if e["status"] == "done")
    total = len(commits)
    return done, total


def current_streak(commits):
    """
    Consecutive 'done' entries counting back from the most recently
    resolved (done/missed) entry, in schedule order.
    """
    resolved = [e for e in commits if e["status"] in ("done", "missed")]
    resolved.sort(key=_scheduled_dt)
    streak = 0
    for e in reversed(resolved):
        if e["status"] == "done":
            streak += 1
        else:
            break
    return streak


def longest_streak(commits):
    resolved = [e for e in commits if e["status"] in ("done", "missed")]
    resolved.sort(key=_scheduled_dt)
    best = running = 0
    for e in resolved:
        if e["status"] == "done":
            running += 1
            best = max(best, running)
        else:
            running = 0
    return best


def check_new_milestone(streak, milestones_seen):
    """Returns the milestone number if `streak` just hit a new one, else None."""
    if streak in MILESTONES and streak not in milestones_seen:
        return streak
    return None


def heatmap_data(commits):
    """
    Returns a list of dicts, one per calendar day in the campaign:
    {"date": "2026-06-12", "status": "done" | "missed" | "pending" | "today" | "mixed"}
    A day is "done" only if every entry that day is done; "missed" if any
    entry that day is missed; "today" if it contains today's date and is
    still in progress; otherwise "pending".
    """
    by_date = {}
    for e in commits:
        by_date.setdefault(e["date"], []).append(e["status"])

    today_str = datetime.now().strftime("%Y-%m-%d")
    out = []
    for d in sorted(by_date.keys()):
        statuses = by_date[d]
        if d == today_str:
            day_status = "today"
        elif any(s == "missed" for s in statuses):
            day_status = "missed"
        elif all(s == "done" for s in statuses):
            day_status = "done"
        else:
            day_status = "pending"
        out.append({"date": d, "status": day_status})
    return out


def next_pending(commits, now=None):
    """Returns the next 'pending' entry by scheduled time, or None."""
    now = now or datetime.now()
    pending = [e for e in commits if e["status"] == "pending"]
    if not pending:
        return None
    pending.sort(key=_scheduled_dt)
    return pending[0]
