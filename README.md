# freelancer-invoicing

Contract-to-invoice pipeline for freelancers: read a contract, track the work,
bill the result — and know at any moment where a project stands.

One Go binary, three stages:

1. **Contract intake.** Upload a contract, get structured data back — client,
   projects, budgets, time frames — review it beside the original, confirm it.
2. **Tracking.** Hours and costs rolled up per project, milestone and task.
3. **Invoicing.** Milestone invoices through free text and a chat interface,
   gated on recorded client approval; hourly invoices from a scanned PDF
   timesheet.

The invoicing core is also exposed over a REST + MCP API for external clients
such as [pocket-cfo](https://github.com/titaniumcoder/pocket-cfo).

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — how it is designed and why:
  the stages in detail, the principles, the planned layout
- [docs/installation.md](docs/installation.md) — run it locally or on Fly.io
- [ROADMAP.md](ROADMAP.md) — the phases, in order
- [CHANGELOG.md](CHANGELOG.md) — what has changed, release by release

## Status

Early alpha, in development at a slow pace. Deployed at
[freelancer-invoicing.fly.dev](https://freelancer-invoicing.fly.dev).

## License

MIT
