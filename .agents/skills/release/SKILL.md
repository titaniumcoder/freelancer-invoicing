---
name: release
description: Cut a release for this repo — convert the CHANGELOG Unreleased section into a tagged GitHub release with those notes. Use when the user asks to release, tag, or publish a version, or after pushing a change that should become a release.
---

# Release

Releases are manual and agent-driven; there is no release workflow. Follow
these steps in order.

1. **Precondition.** `CHANGELOG.md` has entries under `Unreleased`, and every
   doc the changes touched is updated. If not, stop and make that happen
   first — changelog and docs belong to the change, not to the release.
2. **Version.** Read the last `v*` tag (`git tag --list 'v*' --sort=-v:refname
   | head -1`; none means `0.0.0`). Patch bump by default; if the Unreleased
   section contains a `<!-- minor -->` marker, bump the minor instead
   (removing the marker). Versions stay in semver major version zero
   (`0.y.z`) while the project is in alpha.
3. **Changelog.** Move the Unreleased content into a new section
   `## [X.Y.Z] - <today, UTC>` placed after the Unreleased section, and
   restore the empty Unreleased skeleton (Added / Changed / Deprecated /
   Removed / Fixed / Security).
4. **Commit, tag, push.** Commit the changelog as
   `chore(release): vX.Y.Z`, create tag `vX.Y.Z` on that commit, push `main`
   and the tag.
5. **GitHub release.** `gh release create vX.Y.Z --title vX.Y.Z
   --notes-file <file>` where the notes are exactly the new changelog
   section — the changes since the last release, nothing more.
6. **Never rewrite a published section.** If an entry was missed, it goes
   into the next release.

A normal change therefore needs no explicit release step beyond telling the
agent to release: code, changelog, docs, push, then this skill.
