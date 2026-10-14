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
  schema/                  generated types for structured documents
static/
templates/
```

The layout is planned, not built; it will be amended as stages land.

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
