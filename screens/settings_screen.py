"""
screens/settings_screen.py
----------------------------
Simple settings row (PDR 5.7, 7.1 — "no settings maze"): pick one of
3 bundled alarm tones. That's the entire settings surface by design.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

import streak_tracker as st

try:
    from kivy.core.audio import SoundLoader
except ImportError:
    SoundLoader = None

NAVY = (13 / 255, 27 / 255, 42 / 255, 1)
GREEN = (46 / 255, 204 / 255, 113 / 255, 1)
WHITE = (1, 1, 1, 1)

TONES = [
    ("Gentle Bell", "gentle_bell.wav"),
    ("Classic Alarm", "classic_alarm.wav"),
    ("Upbeat Chime", "upbeat_chime.wav"),
]


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        with root.canvas.before:
            Color(*NAVY)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        root.add_widget(Label(text="Alarm Tone", font_size="20sp", bold=True,
                               color=WHITE, size_hint=(1, None), height=dp(36)))

        self.tone_buttons = {}
        for label, filename in TONES:
            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(48), spacing=dp(8))
            btn = Button(text=label, background_color=(0.2, 0.3, 0.4, 1), color=WHITE)
            btn.bind(on_release=lambda inst, f=filename: self._select_tone(f))
            preview = Button(text="\u25b6", size_hint=(None, 1), width=dp(48),
                              background_color=(0.3, 0.35, 0.4, 1), color=WHITE)
            preview.bind(on_release=lambda inst, f=filename: self._preview(f))
            row.add_widget(btn)
            row.add_widget(preview)
            self.tone_buttons[filename] = btn
            root.add_widget(row)

        root.add_widget(BoxLayout())  # spacer

        back_btn = Button(text="Back to Schedule", size_hint=(1, None), height=dp(48),
                           background_color=GREEN, color=WHITE)
        back_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "schedule"))
        root.add_widget(back_btn)

        self.add_widget(root)
        self._root_layout = root

    def _update_bg(self, *args):
        self._bg.pos = self._root_layout.pos
        self._bg.size = self._root_layout.size

    def on_pre_enter(self, *args):
        self._refresh_selection()

    def _refresh_selection(self):
        settings = st.load_settings()
        current = settings.get("alarm_tone", "classic_alarm.wav")
        for filename, btn in self.tone_buttons.items():
            btn.background_color = GREEN if filename == current else (0.2, 0.3, 0.4, 1)

    def _select_tone(self, filename):
        settings = st.load_settings()
        settings["alarm_tone"] = filename
        st.save_settings(settings)
        self._refresh_selection()

    def _preview(self, filename):
        if SoundLoader is not None:
            sound = SoundLoader.load(f"assets/{filename}")
            if sound:
                sound.play()
