"""
screens/schedule_screen.py
---------------------------
Main / home screen (PDR 5.4, 5.6): full 30-day commit list, progress
bar, GitHub-style heatmap, and the idle-mood character.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

import streak_tracker as st
from mood_engine import MoodEngine

NAVY = (13 / 255, 27 / 255, 42 / 255, 1)
GOLD = (244 / 255, 197 / 255, 66 / 255, 1)
GREEN = (46 / 255, 204 / 255, 113 / 255, 1)
GREY = (0.8, 0.8, 0.8, 1)
WHITE = (1, 1, 1, 1)
MISSED_RED = (0.8, 0.3, 0.3, 1)


class HeatmapCell(BoxLayout):
    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        color_map = {
            "done": GREEN,
            "missed": MISSED_RED,
            "today": GOLD,
            "pending": (0.3, 0.35, 0.4, 1),
        }
        with self.canvas.before:
            Color(*color_map.get(status, (0.3, 0.35, 0.4, 1)))
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ScheduleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mood_engine = MoodEngine()
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        with root.canvas.before:
            Color(*NAVY)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        # --- Header: title + character ---
        header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(96))
        title_box = BoxLayout(orientation="vertical")
        title_box.add_widget(Label(text="CommitClock", font_size="22sp", bold=True,
                                    color=WHITE, halign="left", size_hint=(1, None), height=dp(32)))
        self.progress_label = Label(text="0 / 160 commits done", font_size="14sp",
                                     color=GREY, halign="left", size_hint=(1, None), height=dp(24))
        title_box.add_widget(self.progress_label)
        self.progress_bar = ProgressBar(max=160, value=0, size_hint=(1, None), height=dp(14))
        title_box.add_widget(self.progress_bar)
        header.add_widget(title_box)

        self.character_img = Image(source=self.mood_engine.sprite_for("idle"),
                                    size_hint=(None, None), size=(dp(80), dp(80)))
        header.add_widget(self.character_img)
        root.add_widget(header)

        self.streak_label = Label(text="Current streak: 0  |  Best: 0", font_size="14sp",
                                   color=GOLD, size_hint=(1, None), height=dp(24))
        root.add_widget(self.streak_label)

        # --- Heatmap ---
        root.add_widget(Label(text="30-Day Progress", font_size="14sp", color=WHITE,
                               size_hint=(1, None), height=dp(20), halign="left"))
        self.heatmap_grid = GridLayout(cols=10, spacing=dp(3), size_hint=(1, None), height=dp(60))
        root.add_widget(self.heatmap_grid)

        # --- Settings button ---
        settings_btn = Button(text="Alarm Tone Settings", size_hint=(1, None), height=dp(36),
                               background_color=(0.2, 0.3, 0.4, 1), color=WHITE)
        settings_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "settings"))
        root.add_widget(settings_btn)

        # --- Commit list ---
        root.add_widget(Label(text="Full Schedule", font_size="14sp", color=WHITE,
                               size_hint=(1, None), height=dp(20), halign="left"))
        scroll = ScrollView(size_hint=(1, 1))
        self.list_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(2))
        self.list_grid.bind(minimum_height=self.list_grid.setter("height"))
        scroll.add_widget(self.list_grid)
        root.add_widget(scroll)

        self.add_widget(root)
        self._root_layout = root

    def _update_bg(self, *args):
        self._bg.pos = self._root_layout.pos
        self._bg.size = self._root_layout.size

    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        commits = st.load_commits()
        commits = st.mark_missed_if_overdue(commits)
        st.save_commits(commits)

        done, total = st.progress_counts(commits)
        self.progress_label.text = f"{done} / {total} commits done"
        self.progress_bar.max = total
        self.progress_bar.value = done

        cur = st.current_streak(commits)
        best = st.longest_streak(commits)
        self.streak_label.text = f"Current streak: {cur}  |  Best: {best}"

        # idle character mood (could swap to 'excited' on milestone re-entry)
        self.character_img.source = self.mood_engine.sprite_for("idle")

        self._render_heatmap(commits)
        self._render_list(commits)

    def _render_heatmap(self, commits):
        self.heatmap_grid.clear_widgets()
        for day in st.heatmap_data(commits):
            self.heatmap_grid.add_widget(HeatmapCell(day["status"]))

    def _render_list(self, commits):
        self.list_grid.clear_widgets()
        for e in commits:
            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(28))
            mark = {"done": "[color=2ecc71]\u2713[/color]",
                    "missed": "[color=e74c3c]\u2717[/color]",
                    "pending": "[color=cccccc]\u25cb[/color]"}.get(e["status"], "")
            row.add_widget(Label(text=f"{mark} #{e['id']}", markup=True, size_hint=(0.2, 1),
                                  color=WHITE, font_size="12sp"))
            row.add_widget(Label(text=f"{e['date']} {e['time']}", size_hint=(0.3, 1),
                                  color=GREY, font_size="12sp"))
            row.add_widget(Label(text=e["message"], size_hint=(0.5, 1), color=WHITE,
                                  font_size="12sp", halign="left", valign="middle",
                                  text_size=(dp(160), dp(28)), shorten=True))
            self.list_grid.add_widget(row)
