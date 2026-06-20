"""
alarm_service.py
-----------------
Checks the schedule every 30 seconds and fires `on_alarm(entry)` when a
pending commit's scheduled time is reached (within +/-1 minute).

IMPORTANT — read this before relying on it for a real campaign:
This class uses Kivy's Clock, which only runs while the app process is
alive (foreground, or backgrounded-but-not-killed). That is enough for
desktop testing and for short backgrounding on Android.

For alarms that must fire reliably with the screen off / app fully
backgrounded for hours, Android requires a real foreground Service
(AlarmManager + a python-for-android service entry point, declared in
buildozer.spec under `services =`, with a persistent notification and
the FOREGROUND_SERVICE / WAKE_LOCK / VIBRATE / RECEIVE_BOOT_COMPLETED
permissions). That native service glue is platform-specific Java/Pyjnius
code that can't be built or tested in this environment. A stub and
notes for that piece are in widget/android_service_notes.md — treat it
as the next implementation step before shipping the real 30-day run,
and test it on a physical device early (this is flagged as a high-risk
item in the PDR).
"""
from datetime import datetime, timedelta

try:
    from kivy.clock import Clock
except ImportError:  # allows headless testing without a Kivy install
    Clock = None

import streak_tracker as st


class AlarmService:
    def __init__(self, on_alarm, check_interval=30, window_seconds=60):
        """
        on_alarm: callback(entry_dict) invoked once when a commit's
                  scheduled time is reached.
        check_interval: seconds between checks (default 30, per PDR 5.2).
        window_seconds: how close to "now" a scheduled time must be to fire
                  (default 60 = +/-1 min, per PDR 5.2).
        """
        self.on_alarm = on_alarm
        self.check_interval = check_interval
        self.window_seconds = window_seconds
        self._fired_ids = set()
        self._event = None

    def start(self):
        if Clock is not None:
            self._event = Clock.schedule_interval(self._tick, self.check_interval)
        return self._event

    def stop(self):
        if self._event:
            self._event.cancel()
            self._event = None

    def _tick(self, dt):
        self.check_now()

    def check_now(self, now=None):
        now = now or datetime.now()
        commits = st.load_commits()
        for entry in commits:
            if entry["status"] != "pending" or entry["id"] in self._fired_ids:
                continue
            scheduled = datetime.strptime(f"{entry['date']} {entry['time']}", "%Y-%m-%d %H:%M")
            if abs((now - scheduled).total_seconds()) <= self.window_seconds:
                self._fired_ids.add(entry["id"])
                self.on_alarm(entry)

    def snooze(self, entry, minutes=10):
        """Re-arms the alarm to fire again `minutes` from now without
        changing its status (still 'pending')."""
        self._fired_ids.discard(entry["id"])
        if Clock is not None:
            Clock.schedule_once(lambda dt: self.check_now(), minutes * 60)
