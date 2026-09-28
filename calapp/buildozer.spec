[app]
title = 日历仙人
package.name = rilixianren
package.domain = com.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = assets/*.jpg,assets/*.png,saaets/*.ttf
version = 1.0
requirements = python3,kivy==2.3.1,requests,urllib3,chardet,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# ===== 签名配置 =====
android.release_artifact = apk
android.keystore = my-release-key.keystore
android.keystore_pass = 44521667
android.keyalias = my-alias
android.keyalias_pass = 44521667
