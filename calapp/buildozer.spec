[app]
title = 日历仙人
package.name = rilixianren
package.domain = com.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*.jpg,assets/*.png
version = 1.0
requirements = python3,kivy,requests,urllib3,chardet,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.release_artifact = apk
