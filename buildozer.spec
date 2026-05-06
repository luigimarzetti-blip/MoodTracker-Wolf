[app]

title = Mood Tracker Wolf
package.name = moodtrackerwolf
source.include_exts = py,png,jpg,kv,json
icon.filename = icon.png
package.domain = org.luigi
source.dir = .
version = 0.1

# I requisiti corretti con le librerie di traduzione Java
requirements = python3,kivy,android,pyjnius,kivmob

# Impostazioni di visualizzazione sistemate
orientation = portrait
fullscreen = 1

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Permessi di rete e posizione
android.permissions = INTERNET, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION, ACCESS_NETWORK_STATE, com.google.android.gms.permission.AD_ID

# Parametri di sistema Android
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False

# --- CONFIGURAZIONI PER LA PUBBLICITÀ (ADMOB) ---
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-2537033671132924~2254358352
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0
android.enable_androidx = True
