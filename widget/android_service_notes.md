# Android Home-Screen Widget — Notes (Stretch Goal, PDR 5.8)

This is **not implemented** in this build. It's left as documented next
steps because a real AppWidgetProvider requires native Java glue
(via Pyjnius or a small Java module bundled through Buildozer's
`android.add_src`), which can't be authored or tested outside an actual
Android Studio / Buildozer environment.

## What it needs, when you get to it

1. A `RemoteViews`-based widget layout (XML) showing: next commit
   number, date/time, and message — read-only, tap opens the app.
2. A Python-side bridge (Pyjnius) that updates the widget's
   `RemoteViews` whenever `commits.json` changes (e.g. after Submit).
3. `buildozer.spec` additions:
   - `android.add_src = src/android/widget` (or similar) for the Java
     `AppWidgetProvider` subclass and its XML resources.
   - Register the receiver in `AndroidManifest.xml` (Buildozer can
     inject extra manifest entries via `android.manifestPlaceholders`
     or a custom manifest template).
4. Test on a physical device — widgets cannot be verified in an
   emulator-less / Android-tooling-less environment like this one.

## Fallback

Without the widget, the app is fully usable — this only affects the
"see next commit without opening the app" convenience feature (PDR
12, listed explicitly as something that can be dropped if Phase 8
time runs out).
