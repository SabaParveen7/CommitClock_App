"""
screens/alarm_screen.py
-------------------------
Full-screen alarm (PDR 5.3): ringing character + bell, commit number
and message, SUBMIT and Snooze buttons. Reacts with happy/sad mood on
Submit/Snooze, and checks for streak milestones (PDR 5.6) on Submit.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock

import streak_tracker as st
from mood_engine import MoodEngine

try:
    from kivy.core.audio import SoundLoader
except ImportError:
    SoundLoader = None

NAVY = (13 / 255, 27 / 255, 42 / 255, 1)
GREEN = (46 / 255, 204 / 255, 113 / 255, 1)
GOLD = (244 / 255, 197 / 255, 66 / 255, 1)
WHITE = (1, 1, 1, 1)
GREY = (0.8, 0.8, 0.8, 1)


class AlarmScreen(Screen):
    def __init__(self, alarm_service=None, **kwargs):
        super().__init__(**kwargs)
        self.alarm_service = alarm_service
        self.mood_engine = MoodEngine()
        self.current_entry = None
        self._alarm_sound = None
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(14))
        with root.canvas.before:
            Color(*NAVY)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        self.character_img = Image(source=self.mood_engine.sprite_for("ringing"),
                                    size_hint=(1, None), height=dp(200))
        root.add_widget(self.character_img)

        self.commit_number_label = Label(text="Commit #--", font_size="30sp", bold=True,
                                          color=WHITE, size_hint=(1, None), height=dp(48))
        root.add_widget(self.commit_number_label)

        self.commit_message_label = Label(text="", font_size="16sp", color=GREY,
                                           size_hint=(1, None), height=dp(60))
        root.add_widget(self.commit_message_label)

        self.mood_message_label = Label(text="", font_size="14sp", italic=True, color=GOLD,
                                         size_hint=(1, None), height=dp(28))
        root.add_widget(self.mood_message_label)

        root.add_widget(BoxLayout())  # spacer

        self.submit_btn = Button(text="SUBMIT \u2713", font_size="22sp", bold=True,
                                  background_color=GREEN, color=WHITE,
                                  size_hint=(1, None), height=dp(72))
        self.submit_btn.bind(on_release=self.on_submit)
        root.add_widget(self.submit_btn)

        self.snooze_btn = Button(text="Snooze 10 min", font_size="14sp",
                                  background_color=(0.3, 0.35, 0.4, 1), color=WHITE,
                                  size_hint=(1, None), height=dp(40))
        self.snooze_btn.bind(on_release=self.on_snooze)
        root.add_widget(self.snooze_btn)

        self.add_widget(root)
        self._root_layout = root

    def _update_bg(self, *args):
        self._bg.pos = self._root_layout.pos
        self._bg.size = self._root_layout.size

    def show_alarm(self, entry):
        """Called by main.py when alarm_service fires."""
        self.current_entry = entry
        self.commit_number_label.text = f"Commit #{entry['id']}"
        self.commit_message_label.text = entry["message"]
        self.character_img.source = self.mood_engine.sprite_for("ringing")
        self.mood_message_label.text = self.mood_engine.message_for("ringing", entry["id"])
        self.manager.current = "alarm"
        self._play_alarm_tone()

    def _play_alarm_tone(self):
        settings = st.load_settings()
        tone_file = settings.get("alarm_tone", "classic_alarm.wav")
        if SoundLoader is not None:
            self._alarm_sound = SoundLoader.load(f"assets/{tone_file}")
            if self._alarm_sound:
                self._alarm_sound.loop = True
                self._alarm_sound.play()

    def _stop_alarm_tone(self):
        if self._alarm_sound:
            self._alarm_sound.stop()
            self._alarm_sound = None

    def _play_success_chime(self):
        if SoundLoader is not None:
            chime = SoundLoader.load("assets/success_chime.wav")
            if chime:
                chime.play()

    def on_submit(self, *args):
        if not self.current_entry:
            return
        self._stop_alarm_tone()
        self._play_success_chime()

        commits = st.load_commits()
        commits = st.mark_done(commits, self.current_entry["id"])
        st.save_commits(commits)

        settings = st.load_settings()
        cur = st.current_streak(commits)
        settings["current_streak"] = cur
        settings["longest_streak"] = max(settings.get("longest_streak", 0), cur)

        milestone = st.check_new_milestone(cur, settings.get("milestones_seen", []))
        mood = "excited" if milestone else "happy"
        if milestone:
            settings.setdefault("milestones_seen", []).append(milestone)
        st.save_settings(settings)

        self.character_img.source = self.mood_engine.sprite_for(mood)
        self.mood_message_label.text = self.mood_engine.message_for(mood, self.current_entry["id"])

        # brief celebration pause before returning to schedule screen
        Clock.schedule_once(self._return_to_schedule, 2.0)

    def on_snooze(self, *args):
        if not self.current_entry:
            return
        self._stop_alarm_tone()
        self.character_img.source = self.mood_engine.sprite_for("sad")
        self.mood_message_label.text = self.mood_engine.message_for("sad", self.current_entry["id"])
        if self.alarm_service:
            self.alarm_service.snooze(self.current_entry, minutes=10)
        Clock.schedule_once(self._return_to_schedule, 2.0)

    def _return_to_schedule(self, dt):
        self.current_entry = None
        self.manager.current = "schedule"
