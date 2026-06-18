# Contributing

## Branch workflow

- `develop` — default branch, all work happens here
- `main` — release branch, protected (PR only)

Changes are made on `develop` and merged to `main` via pull request
when ready for release.

## PR guidelines

1. Open PRs against the `develop` branch
2. Keep changes focused — one feature/fix per PR
3. Ensure the build succeeds: `./scripts/build.sh`

## Build instructions

```bash
./scripts/build.sh
```

This copies upstream source + Debian packaging into `build/`,
runs `dpkg-buildpackage`, and captures output to `build.log`.

## Commit messages

Use conventional commits format:

```
<type>: <description>

<optional body>
```

Types: `feat`, `fix`, `chore`, `docs`, `packaging`.
