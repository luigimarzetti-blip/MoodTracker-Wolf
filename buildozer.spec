[app]
# Nome e Titolo
title = MoodTracker Wolf
package.name = moodtrackerwolf
package.domain = org.luigimarzetti

# Sorgenti e Estensioni
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# Requisiti (Kivy 2.3.0 è il più stabile per Android 13/14)
requirements = python3,kivy==2.3.0,android,pyjnius,kivmob

# Interfaccia
orientation = portrait
fullscreen = 0

# Icona (Assicurati che icon.png sia presente nella cartella principale)
icon.filename = icon.png

# --- CONFIGURAZIONE ANDROID ---
# Usiamo API 33 (Android 13) per evitare i crash dell'API 34
android.api = 33
android.minapi = 21
android.ndk = 25c
android.accept_sdk_license = True
android.skip_update = False

# Architetture (arm64 è lo standard per i telefoni moderni)
android.archs = arm64-v8a

# Permessi obbligatori per pubblicità e salvataggio
android.permissions = INTERNET, ACCESS_NETWORK_STATE, com.google.android.gms.permission.AD_ID

# --- ADMOB (PUBBLICITÀ) ---
# Sostituisci questo ID con il tuo ID APP reale di AdMob
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-2537033671132924~2254358352
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
