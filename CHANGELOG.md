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

## [0.0.5] - 2026-10-14

### Added

- CI build workflow: build, test, vet and gofmt check on every push to
  `main` and every pull request
- GitHub issues as the tracking convention: non-trivial changes start with
  an issue, commits reference it, the completing commit closes it

### Changed

- Releases and deploys are tag-based: a pushed `v*` tag runs tests first and
  only then deploys to Fly.io; pushes to `main` never release or deploy
- `.agents/skills/release` reworked for the tag flow: it proposes version
  and notes, and tags only after explicit confirmation

### Deprecated

### Removed

### Fixed

### Security

## [0.0.4] - 2026-10-14

### Added

### Changed

- README reduced to a landing document: what the app is, then links to
  architecture, installation, roadmap and changelog — no content repeated

### Deprecated

### Removed

### Fixed

### Security

## [0.0.3] - 2026-10-14

### Added

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — the design document: the
  three stages, principles, planned layout, and where the system is going
  (SaaS: database, object storage)
- `.agents/skills/release` — the release skill; releases are cut manually by
  the agent, not by a workflow

### Changed

- README slimmed down: duplicated descriptions removed, tech stack stated
  without internal references, deployed app linked

### Deprecated

### Removed

- The automatic release workflow and its script; tagging and releasing are
  manual and agent-driven

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

