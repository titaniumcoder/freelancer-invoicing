# Roadmap

Status: **in development, deliberately slow.** This project is a side pipeline
around real client work; progress happens in unhurried passes, one phase at a
time. Phases are sequential — each builds on the one before it.

Markers: ✅ done · 🚧 in progress · ⬜ not started

---

## Phase 0 — Bootstrap ✅

Get the repo ready to think in.

- ✅ README, roadmap, changelog (Keep a Changelog 1.1.0)
- ✅ AGENTS.md — conventions carried over from pocket-cfo and adapted
- ⬜ Go module skeleton: `cmd/` + `internal/` layout, one buildable binary
- ⬜ CI: build + test on push

## Phase 1 — Contract intake ⬜

The stage the repo is named for, and the reason invoicing needs a pipeline in
the first place.

- ⬜ Contract upload and storage of the original document
- ⬜ Parsing a contract into structured data: client, projects, budget per
  project (milestone-based or hourly limits), time frames
- ⬜ Review UI: extracted data presented side by side with the original
  contract, so the user can verify or correct every field
- ⬜ Confirmation as the boundary: only reviewed data becomes records
- ⬜ Chat-style refinement of the extraction (correct a misread budget, add a
  project) before confirming

## Phase 2 — Tracking ⬜

Where the work under a contract is measured.

- ⬜ Define the tracking-source interface (hours, rates, costs, per project /
  milestone / task)
- ⬜ Toggl implementation behind that interface — the only file allowed to
  know Toggl exists
- ⬜ Standing view: budget used vs. budget available per project and
  milestone, hours spent, where each engagement stands

## Phase 3 — Invoicing ⬜

The extracted pocket-cfo core, extended with its two new input paths.

- ⬜ Port the invoicing core from pocket-cfo (documents, rendering, money)
- ⬜ Milestone path: free text + chat interface; the client's approval is
  recorded in the chat and gates invoice creation
- ⬜ Hourly path: scanned PDF timesheet as the invoice source
- ⬜ Explicit non-goal held: no invoice is ever derived from Toggl data

## Phase 4 — pocket-cfo integration ⬜

Close the loop back to where invoicing came from.

- ⬜ REST API over the service layer
- ⬜ MCP surface for the agent side, mirroring pocket-cfo's agent-API pattern
- ⬜ Point pocket-cfo at this app and remove/retire its invoicing half
