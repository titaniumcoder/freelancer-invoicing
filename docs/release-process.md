# Release process

The rule is simple: **every push to `main` that carries changes is a release.**
There is no release branch, no manual tagging, no "we should cut a release
sometime".

## How it works

1. Before pushing, the `Unreleased` section of [CHANGELOG.md](../CHANGELOG.md)
   is updated with everything that changed since the last release. Any
   documentation the change touches (`docs/`, `README.md`, `AGENTS.md`) is
   updated in the same commit.
2. On push, the release workflow
   ([.github/workflows/release.yml](../.github/workflows/release.yml)) does the
   rest:
   - If `Unreleased` has no entries, it does nothing (this covers the
     changelog-editing commit the workflow itself makes).
   - Otherwise it moves the `Unreleased` section into a new dated release
     section, commits that, tags `vX.Y.Z`, and creates a GitHub release whose
     notes are exactly that section — the changes since the last release,
     nothing more.
3. The version number is derived from the previous tag: patch bump by default.
   The workflow never invents content; it only publishes what was written in
   the changelog.

## Versioning

The project follows [Semantic Versioning](https://semver.org). Semver has no
"pre-development" version, but it does define **major version zero**
(`0.y.z`) as initial development: anything may change at any time, the public
API is not stable. That is where this project is, and the numbering reflects
it:

- `0.0.x` — earliest alpha, the shape of the system is still forming
- `0.1.0`, `0.2.0`, … — alpha with recognizable feature milestones
- `1.0.0` — only once the contract → invoice pipeline is complete and stable

The default bump is patch. When a release contains a new feature rather than
fixes and additions to existing work, put a `<!-- minor -->` marker anywhere in
the `Unreleased` section and the workflow bumps the minor version instead.

## In practice

A normal change therefore looks like this:

1. Write the code.
2. Update `CHANGELOG.md` under `Unreleased` (and docs if needed).
3. Commit and push.

The push itself is the release.
