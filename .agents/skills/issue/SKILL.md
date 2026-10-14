---
name: issue
description: Work is tracked in GitHub issues — create an issue for new work, pick up work by issue, reference issues in commits, close issues when done, and keep the ROADMAP checkboxes in sync. Use when planning or starting any task, when the user mentions issues, milestones, or the roadmap, or when a change is bigger than a trivial fix.
---

# issue

All work is tracked in GitHub issues. ROADMAP.md and GitHub mirror each
other: every phase is a milestone, every open roadmap item is an issue with
that milestone. The current state lives in GitHub — the roadmap file is the
written plan, not the tracker.

## Creating an issue

1. Check the roadmap and the open issues first
   (`gh issue list --repo titaniumcoder/freelancer-invoicing`) — the work may
   already be tracked.
2. Non-trivial changes start with an issue:
   `gh issue create --title ... --body ...` with the phase's milestone
   (`--milestone "Phase N — ..."`). The body states what and why, plus
   acceptance criteria. A new roadmap-worthy item also gets a checkbox in
   ROADMAP.md in the same commit that introduces it.
3. Trivial fixes (typos, a one-line doc correction) need no issue — just a
   commit.

## Working on an issue

1. Pick from the current phase's milestone; the order within a phase is
   judgment, dependencies first. `gh issue view N` for the body.
2. Every commit belonging to the issue references it — `(#N)` in the
   subject, and the commit that completes it closes it: `Fixes #N`.
3. The pre-commit checks still apply before pushing: `gofmt -l .`, `go vet
   ./...`, `go build ./...`, `go test ./...`. The Build workflow repeats them
   on push; watch it (`gh run list`, `gh run watch <id> --exit-status`) and
   treat red as a real failure.

## Closing an issue

1. Prefer closing via the commit (`Fixes #N`); otherwise
   `gh issue close N --comment "<what was done>"`.
2. When the issue was a roadmap item, tick its checkbox in ROADMAP.md in the
   same change.
3. An issue closed without the work on `main` is reopened, not forgotten.
   Never close to make a list look shorter.

## Hygiene

- One issue is one deliverable. If it grows a second one, split it.
- Issues are the memory: decisions made while working go into the issue, and
  durable design outcomes go from there into docs/.
- Milestones stay in sync with the roadmap phases: a phase rename changes
  both, together.
