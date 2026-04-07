[app]

# (str) Title of your application
title = VideoDownloaderPro

# (str) Package name
package.name = vdownloader

# (str) Package domain (needed for android packaging)
package.domain = org.alebello

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# MUY IMPORTANTE: certifi y openssl son vitales para que las peticiones HTTPS no fallen
requirements = python3,kivy,requests,certifi,openssl,urllib3,chardet,idna

# (str) Custom source folders for requirements
# (list) Garden requirements
# (str) Presplash of the application
# (str) Icon of the application

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (list) Permissions
# Añadimos permisos de lectura, escritura e internet
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
# API 33 es ideal para Android 13/14
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 33

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android entry point, default is to use start.py
#android.entrypoint = main.py

# (list) Android application meta-data to set (name=value)
# Esto es necesario para que Android permita descargar archivos por HTTP/HTTPS
android.meta_data = android.permission.WRITE_EXTERNAL_STORAGE=1

# (list) Pattern to exclude for the search path
# (list) List of exclusion patterns for the source.dir
# (list) List of directory to exclude for the source.dir

# --- NO TOCAR ESTO ---
[buildozer]
log_level = 2
warn_on_root = 1

# (str) Path to build artifact storage, default is .buildozer
# build_dir = ./.buildozer

# (str) Path to binary target storage, default is bin
# bin_dir = ./bin

