# Maintainers

- Clement Trichet <clement.trichet.pro@gmail.com>

## Source attribution

| Component | Origin | Details |
|-----------|--------|---------|
| Upstream CAMotics | [CauldronDevelopmentLLC/CAMotics](https://github.com/CauldronDevelopmentLLC/CAMotics) | Commit `e84665f` (v1.3.0) |
| Fedora `.spec` reference | [Fedora Koji](https://koji.fedoraproject.org/koji/packageinfo?packageID=22425) | v1.1.1-15 (orphaned/retired) |
| Fedora patches | Extracted from Fedora SRPM | Adapted for Debian build system |
| C! library (cbang) | [CauldronDevelopmentLLC/cbang](https://github.com/CauldronDevelopmentLLC/cbang) | Bundled in upstream source tree |

## Build notes

- Build system: **SCons** (not CMake)
- Qt5 wrapper: `lrelease` is stubbed via `QT5DIR` in `debian/rules`
  (`qttools5-dev-tools` provides the real binary)
- V8: `v8_compress_pointers=0` required for system V8 compatibility
- cbang: built as static library before camotics
