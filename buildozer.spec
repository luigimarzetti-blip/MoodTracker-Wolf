[app]
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Ho rimosso kivmob temporaneamente per testare la stabilità
requirements = python3,kivy==2.3.0,android,pyjnius

orientation = portrait
fullscreen = 0

# Android specific (API 34 è il minimo per il Play Store nel 2026)
android.api = 34
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# Compiliamo solo per arm64 per velocizzare il test su GitHub
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
