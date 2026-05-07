[app]
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti
source.dir = .
# Abbiamo aggiunto 'png' e 'jpg' per le icone degli umori
source.include_exts = py,png,jpg,kv,atlas,json

# --- AGGIUNGI QUESTA RIGA PER L'ICONA ---
icon.filename = icon.png

version = 0.1
requirements = python3,kivy==2.3.0,android,pyjnius
orientation = portrait
fullscreen = 0

# Android config (API 34 è ottima per il 2026)
android.api = 34
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# Architetture: meglio rimettere anche armeabi-v7a per i telefoni più vecchi
android.archs = arm64-v8a, armeabi-v7a

# Permessi (Internet serve se vorrai rimettere KivMob)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
