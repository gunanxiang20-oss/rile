[app]
title = 日历仙人
package.name = rilixianren
package.domain = com.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*.jpg,assets/*.png
version = 1.0
requirements = python3,kivy==2.3.0,requests
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
- name: Install dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y \
      build-essential ccache git libffi-dev libssl-dev python3-dev \
      openjdk-11-jdk unzip automake autoconf libtool pkg-config \
      zlib1g-dev libncurses5-dev libtinfo5 cmake

    python -m pip install --upgrade pip
    python -m pip install "buildozer==1.5.0" "cython<3.0"

- name: Build Release APK
  working-directory: ./calapp
  run: |
    rm -rf .buildozer
    rm -rf bin
    yes | buildozer android release# ===== 签名配置（新增） =====
android.release_artifact = apk
android.keystore = my-release-key.keystore
android.keystore_pass = 44521667
android.keyalias = my-alias
android.keyalias_pass = 44521667
