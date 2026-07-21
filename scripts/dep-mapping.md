# Fedora → Debian Dependency Mapping for Camotics

Derived from `camotics.spec` (Fedora 1.1.1-15) and upstream CAMotics source.

## Build Dependencies

| Fedora Package | Debian Package | Category | Notes |
|---|---|---|---|
| `bzip2-devel` | `libbz2-dev` | build-dep | |
| `desktop-file-utils` | `desktop-file-utils` | build-dep | |
| `gcc-c++` | `g++` | build-dep | Part of `build-essential` |
| `libappstream-glib` | `libappstream-glib-dev` | build-dep | |
| `pkgconfig(cairo)` | `libcairo2-dev` | build-dep | |
| `pkgconfig(dxflib)` | `libdxflib-dev` | build-dep | |
| `pkgconfig(glew)` | `libglew-dev` | build-dep | |
| `pkgconfig(re2)` | `libre2-dev` | build-dep | |
| `pkgconfig(QtCore)` | `qtbase5-dev` | build-dep | Qt5 (pkg-config: Qt5Core) |
| `pkgconfig(QtGui)` | `qtbase5-dev` | build-dep | Qt5 (pkg-config: Qt5Gui) |
| `pkgconfig(QtOpenGL)` | `qtbase5-dev` | build-dep | Qt5 (pkg-config: Qt5OpenGL) |
| `scons` | `scons` | build-dep | |
| `sqlite-devel` | `libsqlite3-dev` | build-dep | |
| `v8-314-devel` | `libnode-dev` (provides v8 headers via `/usr/include/v8/`) | optional | System V8 from Node.js works, but requires `v8_compress_pointers=0` in SCons due to pointer compression mismatch |
| `qttools5-dev-tools` *(Fedora equivalent: `qt5-linguist`)* | `qttools5-dev-tools` | build-dep | Provides `lrelease`; workaround available via QT5DIR stub in `debian/rules` |

## Runtime Dependencies

| Fedora Package | Debian Package | Category | Notes |
|---|---|---|---|
| `qt5-qtbase` | `libqt5widgets5t64`, `libqt5gui5t64`, `libqt5core5t64`, `libqt5network5t64` | runtime-dep | |
| `qt5-qtwebsockets` | `libqt5websockets5` | runtime-dep | |
| `cairo` | `libcairo2` | runtime-dep | |
| `glew` | `libglew2` | runtime-dep | |
| `dxflib` | `libdxflib3` | runtime-dep | |
| `sqlite` | `libsqlite3-0` | runtime-dep | |
| `openssl` | `libssl3t64` | runtime-dep | |
| `nodejs` | `libnode109` (Noble), `libnode127` (Resolute) | runtime-dep | Provides V8 runtime |

## Bundled Libraries (not packaged separately)

| Library | Fedora Handling | Notes |
|---|---|---|
| `cbang` | Bundled (`Provides: bundled(cbang)`) | Patched for system deps |
| `boost` (iostreams, filesystem, system, regex) | Bundled (`Provides: bundled(boost-*)`) | Version 1.63.0 |
| `libevent` | Bundled (`Provides: bundled(libevent)`) | Version 2.1.4 |

## Notes

- `v8-314-devel` excludes `aarch64 ppc64le s390x` on Fedora. In Debian, V8 3.14 is not available. System V8 from `libnode-dev` works but requires `v8_compress_pointers=0` in SCons.
- Ubuntu 26.04 (Resolute) ships Node.js 22 (`libnode127`) and RE2 20250805 (`libre2-10`), compared to Node.js 20 (`libnode109`) and RE2 20240501 (`libre2-9`) on Ubuntu 24.04 (Noble). Runtime dependencies use `shlibs:Depends` and are resolved automatically by dpkg-shlibdeps.
- `lrelease` binary is needed by the Qt5 SCons tool. Install `qttools5-dev-tools`, or use the QT5DIR wrapper workaround in `debian/rules` (symlinks real Qt5 tools + stub lrelease).
- Build uses **SCons**, not CMake (despite some packaging tools defaulting to CMake).
- `cbang` requires extra SCons configuration and is expected to be in `CBANG_HOME` (found in `upstream/camotics/cbang/`).
- `cbang` must be built first with `sharedlib=0` (static lib) before building camotics.
- Most sources listed in `Source0` and `Source1` are already in the upstream repo for version 1.3.0.
