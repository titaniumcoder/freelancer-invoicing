# freelancer-invoicing

Contract-to-invoice pipeline for freelancers: read a contract, track the work,
bill the result — and know at any moment where a project stands.

The invoicing core is extracted from
[pocket-cfo](https://github.com/titaniumcoder/pocket-cfo) and grown into its own
app. Invoicing remains the first and most important part, but around it sits a
pipeline that starts before an invoice ever exists: the contract, and the work
done under it.

One Go binary, three stages:

1. **Contract intake.** Upload a contract; it is parsed into structured data:
   the client, the projects, the budget per project — per milestone or hourly
   limits — and the time frames. The extracted data is presented side by side
   with the original contract for review. Only what the user confirms is
   created; nothing enters the system unreviewed.
2. **Tracking.** Hours, developer rates and costs, rolled up per project,
   milestone and task, so the standing of every engagement is visible at a
   glance. Tracking runs on [Toggl](https://track.toggl.com), but strictly
   behind an internal interface — nothing in the app talks to Toggl directly,
   and the tracking source stays swappable.
3. **Invoicing.** Invoices are never derived from tracking data. Two paths:
   milestone-based contracts are invoiced through free text plus a chat
   interface, and only after the client's approval has been recorded; hourly
   contracts are invoiced from a scanned PDF timesheet.

Because invoicing lives here now, pocket-cfo becomes a client of this app: the
invoicing half is exposed over an API (REST plus an MCP surface for the agent
side) that pocket-cfo consumes.

## Principles

1. **Nothing enters the system unreviewed.** Extracted contract data is a
   proposal until the user has seen it beside the original and confirmed it.
2. **Approval is a first-class fact.** A milestone invoice cannot exist until
   the client's approval is recorded; the chat interface is where that
   approval lives, not a formality in front of it.
3. **Invoices come from humans or scanned PDFs, never from Toggl.** Tracking
   informs where a project stands; it does not generate billing.
4. **Toggl stays behind an interface.** One seam in the code owns the Toggl
   integration; the rest of the app sees a tracking source.
5. **Nothing calculable is stored.** Derived figures — hours used, budget
   remaining, invoice totals — are computed, not persisted.
6. **Money is integer minor units.** `1020000` = 10 200,00 €. No floats.
7. **If something looks suspiciously simple, that's why.** One freelancer, a
   handful of contracts a year, one writer. No locking, no multi-tenancy, no
   workflow engine.

## Tech stack

- **Go**, stdlib first: `net/http` + `html/template`, no router library, no
  framework. Third-party dependencies only where a wire protocol or moving
  external format justifies them (see AGENTS.md for the exceptions and the
  rules that keep them reversible).
- **htmx 4.0.0** for the frontend. Deliberately the current major version,
  not the 2.x line that most examples still show.
- **REST + MCP API** for pocket-cfo, mirroring the agent-API pattern
  pocket-cfo itself uses.

## Planned layout

```
cmd/
  freelancer-invoicing/    web app
  fi-ctl/                  CLI — pipeline steps, identical locally and in CI
internal/
  contracts/               intake: parse → review → confirm
  tracking/                the Toggl interface and its one implementation
  invoicing/               the extracted pocket-cfo invoicing core
  api/                     REST + MCP adapters over the service layer
  schema/                  generated types for structured documents
static/
templates/
```

The layout is planned, not built; it will be amended as stages land.

## Status

In development, deliberately at a slow pace. See
[ROADMAP.md](ROADMAP.md) for the phases and
[CHANGELOG.md](CHANGELOG.md) for what has changed so far.

Every push to `main` is automatically tagged and released; running the app
locally is covered in [docs/installation.md](docs/installation.md).

## License

MIT
