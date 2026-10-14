# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.0.2] - 2026-10-14

### Added

### Changed

- Release rules moved from `docs/release-process.md` into `AGENTS.md`:
  releasing is a convention the agent follows, not user-facing documentation.
  How others solve releases is their problem.

### Deprecated

### Removed

### Fixed

### Security

## [0.0.1] - 2026-10-14

### Added

- Project bootstrap: README, ROADMAP, CHANGELOG, AGENTS.md
- Deployment setup: Dockerfile, `fly.toml` (region `fra`, auto-stop with zero
  minimum machines), and a GitHub Actions deploy workflow on push to `main`
- [docs/installation.md](docs/installation.md) — how to run the app locally
  with Go or Docker, and on Fly.io
- Automatic releases: every push to `main` with changelog entries is tagged
  and published as a GitHub release, with notes taken from the `Unreleased`
  section of this file

### Changed

### Deprecated

### Removed

### Fixed

### Security

