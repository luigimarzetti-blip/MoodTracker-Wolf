[app]
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# ATTENZIONE: kivmob richiede spesso permessi specifici e internet
requirements = python3,kivy==2.3.0,android,pyjnius,kivmob

orientation = portrait
fullscreen = 0

# Android specific
android.api = 34
android.minapi = 21
# Lasciamo vuoti questi per farli gestire a Buildozer nel cloud
# android.sdk_path = 
# android.ndk_path = 

# Architetture necessarie per il Play Store e test moderni
android.archs = arm64-v8a, armeabi-v7a

# Permessi necessari per KivMob/AdMob
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (Opzionale) Se usi KivMob, inserisci qui l'App ID di test o reale
# android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

[buildozer]
log_level = 2
warn_on_root = 1
