# CAMotics Debian Packaging for Ubuntu

**Target distribution: Ubuntu 24.04 (Noble Numbat)**

Debian packaging for [CAMotics](https://camotics.org/) v1.3.0 — an
open-source 3-axis CNC machining simulation software. This repository
produces a `.deb` package for easy installation on Ubuntu.

> **Note**: This package is built and tested on Ubuntu 24.04 only.
> It may not work on Debian or older Ubuntu releases due to library
> version differences.

## Build from source

```bash
sudo apt install scons debhelper qtbase5-dev libglew-dev libcairo2-dev \
  libdxflib-dev libre2-dev libbz2-dev libsqlite3-dev \
  libqt5websockets5-dev pkgconf libappstream-glib-dev
./scripts/build.sh
```

The `.deb` will be in the `build/` directory.

## Install

```bash
sudo dpkg -i build/camotics_1.3.0-1_amd64.deb
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
