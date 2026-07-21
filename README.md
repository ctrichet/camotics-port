# CAMotics Debian Packaging for Ubuntu & Debian

**Target distributions: Ubuntu 24.04 (Noble Numbat), Ubuntu 26.04 (Resolute Racoon), and Debian 12 (Bookworm)**

Debian packaging for [CAMotics](https://camotics.org/) v1.3.0 — an
open-source 3-axis CNC machining simulation software. This repository
produces a `.deb` package for easy installation on Ubuntu and Debian.

## Build from source

### Ubuntu Noble

```bash
sudo apt install scons debhelper qtbase5-dev libglew-dev libcairo2-dev \
  libdxflib-dev libre2-dev libbz2-dev libsqlite3-dev \
  libqt5websockets5-dev pkgconf libappstream-glib-dev
./scripts/build.sh --distro noble
```

### Ubuntu Resolute

```bash
sudo apt install scons debhelper qtbase5-dev libglew-dev libcairo2-dev \
  libdxflib-dev libre2-dev libbz2-dev libsqlite3-dev \
  libqt5websockets5-dev pkgconf libappstream-glib-dev
./scripts/build.sh --distro resolute
```

### Debian Trixie

```bash
sudo apt install scons debhelper qtbase5-dev libglew-dev libcairo2-dev \
  libdxflib-dev libre2-dev libbz2-dev libsqlite3-dev \
  libqt5websockets5-dev pkgconf libappstream-glib-dev
./scripts/build.sh --distro bookworm
```

The `.deb` will be in the `build/` directory.

## Install

```bash
# The .deb filename varies by version and distribution; check build/ for the exact name.
sudo dpkg -i build/camotics_*.deb
```

## Usage

```bash
# GUI
camotics

# CLI simulation (requires a G-code or TPL file)
camsim examples/box/box.tpl output.stl

# G-code inspection
gcodetool --help

# Tool path planning
planner --help
```

## License

LGPL-2.1-or-later (same as upstream CAMotics).
