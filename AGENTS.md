# AGENTS.md

This repo has no `ARCHITECTURE.md` yet; until one exists, this file and
`README.md` together are the canonical description of the design. When
`ARCHITECTURE.md` appears, design content moves there and this file goes back
to recording only conventions that aren't obvious from the code itself.

## What this is

The contract-to-invoice pipeline extracted from pocket-cfo: contract intake →
tracking → invoicing, with the invoicing core served back to pocket-cfo over a
REST + MCP API. `README.md` states the three stages and the principles; the
conventions below apply across all of them.

## Conventions

- **Stdlib first.** Only reach for a third-party dependency when there is a
  genuinely strong reason: `net/http` + `html/template`, no router library.
  Named exceptions, each held to three rules — imported by exactly one file,
  no SDK/library type crossing past that file into the service layer, and
  tests that drive a stub with hand-written data so a hand-rolled replacement
  would be equally validated:
  - `htmx`, pinned to **4.0.0** — the current major version, chosen
    deliberately over the 2.x line that most examples still show. Frontend
    only; it appears in `templates/`/`static/`, never in Go imports.
  - `github.com/modelcontextprotocol/go-sdk` for the MCP surface at `/mcp`,
    same rationale as in pocket-cfo: a moving external wire protocol whose
    failure mode is silence. Tool names, descriptions and schemas live
    SDK-free beside the REST handlers so the two adapters cannot drift.
  - an OpenAI-compatible client for the LLM calls (contract parsing, scanned
    PDF reading), same three rules.
  - `go-jsonschema` as a dev-time `tool` dependency to generate Go structs
    from `schemas/*.json` — never imported by runtime code.
- **The code explains itself; comments do not.** Go code here carries no
  comments. When a block needs explaining, extract it into a function whose
  name is the explanation, or name the constant, or split the function until
  each piece is obvious.
- **Nothing enters the system unreviewed.** Contract extraction produces a
  proposal displayed beside the original document; only user-confirmed data
  becomes a record. Code must not create records from parsed input directly.
- **Toggl stays behind one interface.** Exactly one file may import a Toggl
  client or know Toggl's API shape; everything else sees the internal
  tracking-source interface. This is the same three-rules discipline as the
  other exceptions, so the tracking source stays swappable.
- **Invoices are never derived from tracking data.** The two inputs are free
  text plus the chat interface (milestone path, gated on recorded client
  approval) and a scanned PDF timesheet (hourly path). No code path may
  connect the tracking source to invoice generation.
- **Approval is a first-class fact.** A milestone invoice cannot be created
  until the client's approval exists as a recorded fact in the system. The
  check belongs in the service layer, not the UI.
- **Nothing calculable is stored.** Hours used, budget remaining, invoice
  totals — computed on read, never persisted, so nothing can disagree with
  its own inputs.
- **Money is integer minor units.** `1020000` = 10 200,00 €. No floats.
- **Schema documents are `go:embed`ed**, never read from disk at runtime,
  and every structured data shape gets generated Go types via `go-jsonschema`
  — never a hand-written struct for a data shape.
- **Persistent state changes go through git.** Whatever the storage shape
  turns out to be, a change is a commit with an author and a date; git
  history is the audit trail, not an appended log field.
- **Simple, on purpose.** One freelancer, a handful of contracts a year, one
  writer: no locking, no multi-tenancy, no workflow engine. If a design
  looks suspiciously simple, that is the reason, not an oversight.
- **Every push to `main` is a release.** Before pushing, `CHANGELOG.md`
  (section `Unreleased`) and any docs the change touches are updated in the
  same commit; the release workflow turns that section into a tagged GitHub
  release. Versions are semver in major version zero while in alpha — see
  `docs/release-process.md`.
