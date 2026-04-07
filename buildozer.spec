[app]
title = VideoDownloaderPro
package.name = vdownloader
package.domain = org.alebello

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# Dependencias limpias y estables
requirements = python3,kivy==2.2.1,requests,certifi,urllib3,idna,chardet

orientation = portrait

# Permisos (compatibles con Android moderno + fallback)
android.permissions = INTERNET, READ_MEDIA_VIDEO, READ_MEDIA_IMAGES, READ_MEDIA_AUDIO, WRITE_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21

# IMPORTANTE: para que los archivos se vean
android.private_storage = False

[buildozer]
log_level = 2
warn_on_root = 1
