[app]

title = Mood Tracker Wolf
package.name = moodtrackerwolf
source.include_exts = py,png,jpg,kv,json
icon.filename = icon.png
package.domain = org.luigi
source.dir = .
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.permissions = INTERNET, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION

# --- AGGIUNGI QUESTE RIGHE SOTTO ---
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False