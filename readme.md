<div align="center">

# snolcNG

desktop and Android client for [snolc](https://github.com/owenewans/snolc).

<a href="https://count.owenewans.org/owenewans/snolcNG?theme=moebooru-h&notitle"><img src="https://count.owenewans.org/owenewans/snolcNG?theme=moebooru-h&notitle" alt="repository views"></a>

`rust` `android` `egui`

</div>

## build

Clone the module submodule, then build with Rust 1.98.1:

```sh
git clone --recurse-submodules https://github.com/owenewans/snolcNG
cd snolcNG
cargo build --locked --release
```

Build the Android APK with API 36 and NDK 29:

```sh
cd android
./gradlew --no-daemon assembleDebug
```

The APK contains `libsnolc_ng.so` and ten module libraries for armv7 and
aarch64. Android 7.0, API 24, is the minimum release.

## profiles

The client imports strict `snolc://profile/` URIs and subscription documents.
It limits profile input to 64 KiB, subscription input to 1 MiB and each
subscription to 64 profiles. The client writes profile files through a
temporary file and rename.

The Android service passes its TUN file descriptor to `adapter-tun`. Desktop
and Android run the same engine and profile code.

## source boundaries

This repository pins the core engine by commit. The `snolc-modules` submodule
pins the native libraries used in Android packages. Update either pin through a
pull request and run both desktop and APK gates.

## license

[Unlicense](LICENSE)
