[app]
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# RIGA MANCANTE AGGIUNTA QUI:
version = 0.1

# Requisiti minimi per testare se compila
requirements = python3,kivy==2.3.0,android,pyjnius

orientation = portrait
fullscreen = 0

# Android specific
android.api = 34
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
