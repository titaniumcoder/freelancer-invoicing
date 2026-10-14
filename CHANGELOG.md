# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Conventional Commits for messages on `main`; the release version is now
  derived from them — `feat` means minor, a breaking marker means major,
  everything else is patch-level
- docs/ARCHITECTURE.md gains a "Data scheme" section as a TODO marker: the
  storage schema (contracts, milestones, approvals, invoices) will be
  documented there once it takes shape

### Changed

- README documentation section links the changelog format and the commit
  convention; the release skill derives the version from commits instead of
  a marker in the changelog
- docs/installation.md is for running the app locally only; the Fly deploy
  instructions moved out — deploys are the GitHub Actions' job on a release
  tag, never a manual step
- No JSON Schema in this project: records live in a database, documents are
  PDFs, and JSON appears only at the API boundary; if the API needs a
  published contract, whole API tooling (e.g. OpenAPI) instead of
  schema-generated types. The go-jsonschema exception and the `schema/`
  planned layout entry are gone
- ROADMAP reordered around what matters first: Phase 0 (bootstrap) gains the
  Postgres database layer (local development, deployed on Neon.tech), then
  invoicing, pocket-cfo integration, contract intake, and Toggl tracking
  last
- ROADMAP gains a dashboard phase after invoicing: a mini CRM with clients,
  earnings, open points and the contract pipeline; pocket-cfo integration,
  contract intake and tracking shift back one phase each
- Phase 0 gains the SaaS groundwork as evaluations: login providers, billing
  for B2B and B2C in Europe, and tracking/logs/statistics — ten
  GDPR-compatible candidates each — followed by implementing the chosen
  platforms
- Evaluation stance sharpened: managed services only (self-hosting is a
  distraction), billing narrowed to Paddle vs Stripe (merchant of record vs
  processor), Sentry the error-tracking frontrunner; product analytics and
  logs still to pick
- Neon Auth (managed Better Auth in the Neon database, branchable) joins the
  login candidates; Supabase stays in the database comparison as the
  database-plus-auth bundle; billing tilted toward Paddle since handling VAT
  oneself is a pain the project avoids
- docs/ARCHITECTURE.md "Immutable documents" section: render-once rule,
  SHA-256 stored with the invoice and embedded in the object key, Tigris
  versioning as backstop (Object Lock later if SaaS stakes demand it, AWS S3
  has compliance-mode WORM), PDF/A as readability not integrity, PAdES
  deferred, and the confidentiality rules for the document store
- Immutable-documents layer 1 refined to the pocket-cfo model: invoices live
  as freely editable drafts until issued; issuing renders the PDF once and
  freezes the record; afterwards only storno/revision documents, with a
  documented reissue as the exceptional escape hatch
- Document storage decided: AWS S3 with versioning and compliance-mode
  Object Lock (WORM) instead of Tigris — a trust decision for long-term
  storage; PDF/A is mandatory for the ten-year retention; signing deferred
  with the two paths spelled out (platform-signed is easy, client-signed
  means certificate integration)

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

