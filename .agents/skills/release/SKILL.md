---
name: release
description: Propose and cut a tagged release — convert the CHANGELOG Unreleased section into a version section, tag it, and publish the GitHub release with those notes. Use when the user asks to release, tag, or publish a version. Never tag or push a release without this skill's confirmation step.
---

# release

Releases are tags. A push to `main` never releases and never deploys; a pushed
`v*` tag is what triggers the Deploy workflow (tests run first, then Fly) and
what the GitHub release hangs off. Never tag or push a release without the
confirmation step in Phase 3 — a tag is a visible, hard-to-reverse action.

## Phase 1 — Gather state

1. `git status --short` — the working tree should be clean. If not, stop and
   say what is uncommitted; do not release from dirty state.
2. `git fetch origin --tags`, then check for unpushed commits
   (`git log origin/main..HEAD --oneline`). Flag them in the proposal; they
   must reach `origin/main` before or alongside the tag.
3. Precondition: `CHANGELOG.md` has entries under `Unreleased`, and every doc
   the changes touched is updated. If not, that belongs to the change — make
   it happen first.

## Phase 2 — Propose

1. Version: read the last `v*` tag (`git tag --list 'v*' --sort=-v:refname |
   head -1`; none means `0.0.0`). Patch bump by default; if the Unreleased
   section contains a `<!-- minor -->` marker, bump the minor instead
   (removing the marker). Versions stay in semver major version zero
   (`0.y.z`) while the project is in alpha.
2. Show the proposal: the version and the `Unreleased` entries as they will
   appear in the release notes.
3. Ask for explicit confirmation. No confirmation, no tag — say so and stop.

## Phase 3 — Cut

On confirmation only:

1. Move the Unreleased content into a new section `## [X.Y.Z] - <today, UTC>`
   placed after the Unreleased section, and restore the empty Unreleased
   skeleton (Added / Changed / Deprecated / Removed / Fixed / Security).
   **Footgun:** after a release, `Unreleased` is empty, so a changelog edit
   whose context matches section headers can land in the released section
   below instead. When adding an entry, always target the text right under
   `## [Unreleased]` and re-read the file afterwards to confirm the entry
   sits there and published sections are untouched.
2. Commit as `chore(release): vX.Y.Z`, tag `vX.Y.Z` on that commit, push
   `main` and the tag. Before tagging, re-read the file: it must already
   contain the new `## [X.Y.Z]` section and an empty Unreleased — tagging
   without the conversion leaves the file out of sync with the release.
3. Create the GitHub release: `gh release create vX.Y.Z --title vX.Y.Z
   --notes-file <file>` where the notes are exactly the new changelog
   section — the changes since the last release, nothing more.
4. Watch the Deploy workflow for the tag
   (`gh run list` then `gh run watch <id> --exit-status`) and report whether
   tests passed and the deploy went out. A red run is a real failure to fix,
   not a footnote.

## After

Never rewrite a published section. If an entry was missed, it goes into the
next release.
