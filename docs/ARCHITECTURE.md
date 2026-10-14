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
   glance. Tracking lives in the app natively — a timer and entries — with
   Toggl available as an additional source; both sit strictly behind an
   internal tracking-source interface, and exactly one file knows Toggl
   exists.
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

1. **Draft until issued, rendered once at issue.** Carried over from
   pocket-cfo, where it worked in practice: an invoice starts as a draft that
   can be changed as often as needed — nothing is immutable while it is a
   draft, and no PDF exists yet. Issuing renders the PDF exactly once and
   freezes the record. After that, corrections are new documents (a storno
   or a revision); the escape hatch for an issued document that is truly
   wrong is a documented reissue — an exceptional, audited act, needed
   exactly once in pocket-cfo's history.
2. **Hash as the address.** The SHA-256 of the PDF bytes is stored with the
   invoice record in Postgres, and the object key contains that hash
   (`invoices/<hash>.pdf`). An overwritten object would move to a different
   address, so any mismatch between the stored hash and the served bytes is
   tampering, detected on every read. Standard library only
   (`crypto/sha256`).
3. **Storage on AWS S3, not Tigris.** Long-term storage is a trust decision:
   the documents go to AWS S3, where object versioning plus compliance-mode
   Object Lock give a hard WORM guarantee — nobody, including the account
   owner, can delete or overwrite a locked object before the retention ends
   (set to cover the ten-year retention window). At this project's volume
   (~1 GB over ten years) the cost is rounding error money; Object Lock
   itself is a bucket feature, not a paid tier.
4. **Sealing, when needed.** Signing is kept for later, and there are two
   distinct paths when it comes: the platform signs (easy — an Ed25519 key
   of the app, or a PAdES signature with a certificate the platform holds),
   or the client signs (hard — certificate integration, key custody, HSM or
   smartcard questions). Candidate tooling for the platform path exists
   (`digitorus/pdfsign`); the decision is deferred until a client or
   authority actually demands a signature.
5. **PDF/A is mandatory.** The documents must stay readable for ten years,
   and a lot changes in ten years — renderers, fonts, viewers. Generating
   PDF/A-2b (or better) is therefore a requirement of the rendering step,
   not an option. As stated: this is about long-term readability, not
   tamper-proofing — the layers above handle integrity.

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
