[app]
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# Requisiti essenziali
requirements = python3,kivy==2.3.0,android,pyjnius,kivmob

orientation = portrait
fullscreen = 0
icon.filename = icon.png

# --- CONFIGURAZIONE ANDROID ---
android.api = 33
android.minapi = 21
android.ndk = 25c
android.accept_sdk_license = True
android.skip_update = False
android.archs = arm64-v8a

# Permessi e Pubblicità
android.permissions = INTERNET, ACCESS_NETWORK_STATE, com.google.android.gms.permission.AD_ID
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-2537033671132924~2254358352
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
