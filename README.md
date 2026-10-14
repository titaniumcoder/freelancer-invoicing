# freelancer-invoicing

Contract-to-invoice pipeline for freelancers: read a contract, track the work,
bill the result — and know at any moment where a project stands.

One Go binary, three stages:

1. **Contract intake.** A contract is parsed into structured data — client,
   projects, budgets, time frames — and shown beside the original for review.
   Only confirmed data becomes a record.
2. **Tracking.** Hours and costs rolled up per project, milestone and task,
   so every engagement's standing is visible at a glance.
3. **Invoicing.** Milestone contracts through free text and a chat interface,
   gated on recorded client approval; hourly contracts from a scanned PDF
   timesheet. Never derived from tracking data.

The invoicing core is exposed over a REST + MCP API for external clients such
as [pocket-cfo](https://github.com/titaniumcoder/pocket-cfo).

## Invariants

- Nothing enters the system unreviewed.
- Approval is a first-class fact: no milestone invoice without recorded
  client approval.
- Invoices come from humans or scanned PDFs, never from tracking data.
- Toggl stays behind one interface.
- Nothing calculable is stored.
- Money is integer minor units: `1020000` = 10 200,00 €.
- Suspiciously simple on purpose: one freelancer, no multi-tenancy.

## Tech stack

- Go, stdlib first. Third-party dependencies where they earn their place —
  object storage and a database are coming as the project grows into a SaaS.
- htmx for the frontend for now; flexible there.
- Design details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Status

Early alpha, in development at a slow pace. Deployed at
[freelancer-invoicing.fly.dev](https://freelancer-invoicing.fly.dev) — it
sleeps when idle and wakes on the first request. To run it yourself see
[docs/installation.md](docs/installation.md); recent changes in
[CHANGELOG.md](CHANGELOG.md); the phases in [ROADMAP.md](ROADMAP.md).

## License

MIT
