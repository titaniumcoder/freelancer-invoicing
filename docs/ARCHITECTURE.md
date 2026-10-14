# Architecture

The design of the contract-to-invoice pipeline. Conventions the code must
follow live in [AGENTS.md](../AGENTS.md); this document describes what the
system is and why.

## What this is

A pipeline for one freelancer: contract intake → tracking → invoicing, served
as one Go binary with a web UI. The invoicing core is additionally exposed
over a REST + MCP API for external clients such as pocket-cfo.

## The three stages

1. **Contract intake.** Upload a contract; it is parsed into structured data:
   the client, the projects, the budget per project — per milestone or hourly
   limits — and the time frames. The extracted data is presented side by side
   with the original contract for review; chat-style refinement (correct a
   misread budget, add a project) happens before confirmation. Only what the
   user confirms is created; nothing enters the system unreviewed.
2. **Tracking.** Hours, developer rates and costs, rolled up per project,
   milestone and task, so the standing of every engagement is visible at a
   glance. Tracking runs on Toggl, but strictly behind an internal
   tracking-source interface — exactly one file knows Toggl exists, and the
   source stays swappable.
3. **Invoicing.** Invoices are never derived from tracking data. Two paths:
   milestone-based contracts are invoiced through free text plus a chat
   interface, and only after the client's approval has been recorded as a
   fact; hourly contracts are invoiced from a scanned PDF timesheet.

## Principles

1. **Nothing enters the system unreviewed.** Extracted contract data is a
   proposal until the user has seen it beside the original and confirmed it.
2. **Approval is a first-class fact.** A milestone invoice cannot exist until
   the client's approval is recorded; the check belongs in the service layer,
   not the UI.
3. **Invoices come from humans or scanned PDFs, never from Toggl.** Tracking
   informs where a project stands; it does not generate billing.
4. **Nothing calculable is stored.** Derived figures — hours used, budget
   remaining, invoice totals — are computed, not persisted.
5. **Money is integer minor units.** `1020000` = 10 200,00 €. No floats.
6. **Persistent state changes go through git.** Whatever the storage shape
   turns out to be, a change is a commit with an author and a date; git
   history is the audit trail, not an appended log field.
7. **If something looks suspiciously simple, that's why.** One freelancer, a
   handful of contracts a year, one writer. No locking, no multi-tenancy, no
   workflow engine.

## Planned layout

```
cmd/
  freelancer-invoicing/    web app
  fi-ctl/                  CLI — pipeline steps, identical locally and in CI
internal/
  contracts/               intake: parse → review → confirm
  tracking/                the Toggl interface and its one implementation
  invoicing/               the invoicing core
  api/                     REST + MCP adapters over the service layer
static/
templates/
```

The layout is planned, not built; it will be amended as stages land.

## Data scheme

TODO. The storage schema for the records the pipeline keeps — contracts,
projects, milestones, recorded approvals, invoices — will be documented here
once it takes shape. Until then, nothing is fixed: the shape is still being
discovered, and nothing calculable is stored in any case (see Principles).

## Immutable documents

An issued invoice must not change — not because someone might edit a file,
but because the record it attests must stay verifiable for years (German
GoBD expects ten-year retention with integrity assurance; documented internal
controls are accepted, a qualified signature is not mandatory). The design is
layered, cheapest layer first:

1. **Rendered once, never mutated.** An invoice PDF is written exactly once,
   at creation. A correction produces a new document (a storno or revision);
   the old file is never touched. This is an application rule, not a feature.
2. **Hash as the address.** The SHA-256 of the PDF bytes is stored with the
   invoice record in Postgres, and the object key contains that hash
   (`invoices/<hash>.pdf`). An overwritten object would move to a different
   address, so any mismatch between the stored hash and the served bytes is
   tampering, detected on every read. Standard library only
   (`crypto/sha256`).
3. **Storage backstop.** The document bucket keeps object versioning and
   snapshots enabled, so every write persists. Tigris (Fly's object storage,
   billed on the same bill) supports versioning and snapshots but has no
   Object Lock; AWS S3's compliance-mode Object Lock is the hard WORM
   guarantee. At this project's volume (~1 GB over a ten-year retention
   window) both cost rounding error money, so the choice is about complexity,
   not price: start on Tigris, and the storage seam stays swappable so an
   Object-Lock-capable archival bucket can be added when the SaaS stakes
   make it worthwhile.
4. **Sealing, when needed.** A detached Ed25519 signature over the stored
   hash, verifiable offline, proves integrity even against storage-side
   manipulation — with the honest limit that as long as the app holds the
   key, it proves the chain, not non-repudiation. A PAdES signature inside
   the PDF (candidate tooling: `digitorus/pdfsign`) is a deliberate,
   deferred dependency, taken only if a client or authority demands one.
5. **PDF/A is readability, not integrity.** Generating PDF/A-2b serves the
   ten-year archive readability requirement; it does not make a document
   tamper-proof. It is a detail of the rendering step, not a security layer.

Confidentiality is a separate requirement from immutability: nobody should be
able to see or guess another party's invoices. Rules for the document store
and the service layer:

- The bucket is private — no public access, no directory listing; all access
  goes through the service layer, which checks ownership per record.
- Object keys are unguessable: random IDs (or the content hash), never
  sequential numbers.
- Direct downloads, when needed, go through short-lived presigned URLs only.
- Every record is scoped to its owner from day one — the multi-tenancy the
  simplicity principle rules out for workflows is not an excuse for one
  tenant's data leaking into another's.

## Where the system is going

The pipeline currently serves one freelancer, but it grows into a SaaS. That
direction is already visible in the design: a database is needed for the
whole part (contracts, invoices, recorded approvals), and object storage
(e.g. S3) for original documents and scanned timesheets. The
simplicity principle above applies to the current stage, not to the end
state — the seams (tracking source, storage, database) are chosen so these
can be added without reworking the core.

## Deployment

Deployed on Fly.io at `freelancer-invoicing.fly.dev`, region `fra`, one
shared-cpu-1x machine with 256 MB. The machine sleeps when idle
(`min_machines_running = 0`, auto-stop) and wakes on the first request.
Every push to `main` runs the Build workflow (build, vet, test, format);
nothing publishes or deploys from it. Deploys happen only on a version tag
push ([.github/workflows/deploy.yml](../.github/workflows/deploy.yml)), and
only after the same checks pass there. How to run it locally:
[installation.md](installation.md).
