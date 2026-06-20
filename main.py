"""
main.py
-------
CommitClock entry point (PDR section 8.2).

Run on desktop for development/testing:
    pip install kivy
    python main.py

Build an Android APK (on a Linux machine with Buildozer installed):
    buildozer -v android debug
See README.md for full instructions and current limitations.
"""
import os
import sys

# Make sure local imports (streak_tracker, mood_engine, screens/) resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from screens.schedule_screen import ScheduleScreen
from screens.alarm_screen import AlarmScreen
from screens.settings_screen import SettingsScreen
from alarm_service import AlarmService


class CommitClockApp(App):
    title = "CommitClock"

    def build(self):
        Window.clearcolor = (13 / 255, 27 / 255, 42 / 255, 1)

        self.sm = ScreenManager(transition=FadeTransition(duration=0.15))

        self.schedule_screen = ScheduleScreen(name="schedule")
        self.alarm_screen = AlarmScreen(name="alarm")
        self.settings_screen = SettingsScreen(name="settings")

        self.sm.add_widget(self.schedule_screen)
        self.sm.add_widget(self.alarm_screen)
        self.sm.add_widget(self.settings_screen)

        self.alarm_service = AlarmService(on_alarm=self._on_alarm)
        self.alarm_screen.alarm_service = self.alarm_service
        self.alarm_service.start()

        return self.sm

    def _on_alarm(self, entry):
        self.alarm_screen.show_alarm(entry)


if __name__ == "__main__":
    CommitClockApp().run()
