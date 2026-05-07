[app]
# ... (il resto rimane uguale)
version = 0.1

# Requisiti
requirements = python3,kivy==2.3.0,android,pyjnius

# Android settings - Svuota i percorsi se avevi messo roba strana
android.api = 34
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
