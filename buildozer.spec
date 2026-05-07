[app]
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Riduciamo al minimo indispensabile. Se compila così, aggiungeremo il resto dopo.
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Android specific
android.api = 34
android.minapi = 21
# Forziamo una versione specifica dell'NDK che sappiamo funzionare
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# Compiliamo solo per una architettura per non farlo durare ore
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
