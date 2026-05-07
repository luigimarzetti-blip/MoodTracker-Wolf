[app]
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.3.0,android,pyjnius,kivmob
orientation = portrait
fullscreen = 0
icon.filename = icon.png

# Configurazione Android
android.api = 34
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Metadata per AdMob (Pubblicità)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

[buildozer]
log_level = 2
warn_on_root = 1
