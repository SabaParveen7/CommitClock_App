[app]
title = CommitClock
package.name = commitclock
package.domain = org.personal

source.dir = .
source.include_exts = py,png,jpg,jpeg,wav,json,kv,atlas

version = 2.0

requirements = python3,kivy

# Portrait phone app
orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/character_idle.png

# --- Android specifics ---
android.permissions = VIBRATE, WAKE_LOCK, FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED, SYSTEM_ALERT_WINDOW
android.api = 33
android.minapi = 28
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# NOTE: true reliable background alarm firing (screen off, app fully
# backgrounded for hours) requires a python-for-android foreground
# Service entry point declared here, e.g.:
#   services = AlarmCheck:alarm_service_android.py
# That native service file is NOT included in this build — see
# widget/android_service_notes.md and the README "Known Limitations"
# section before relying on this for the real 30-day campaign.

[buildozer]
log_level = 2
warn_on_root = 1
