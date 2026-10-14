# Roadmap

Status: **in development, deliberately slow.** This project is a side pipeline
around real client work; progress happens in unhurried passes, one phase at a
time. Phases are sequential — each builds on the one before it.

Markers: ✅ done · 🚧 in progress · ⬜ not started

---

## Phase 0 — Bootstrap 🚧

Get the repo ready to think and build in.

- ✅ README, ROADMAP, CHANGELOG, AGENTS.md, ARCHITECTURE
- ✅ Go module and a first serving binary
- ✅ Deployment setup: Dockerfile, Fly (auto-stop, zero idle machines)
- ✅ CI: build, test, vet and format check on push; deploys and releases on
  version tags only
- ⬜ Postgres database layer: schema and access for the records the pipeline
  keeps, runnable locally for development and deployed on Neon.tech
- ⬜ Evaluate login providers — GDPR-compatible candidates: Ory, Zitadel,
  Hanko, Keycloak, Authentik, Stack Auth, Supabase Auth, Clerk, Auth0, Kinde
- ⬜ Evaluate billing for B2B and B2C in Europe (VAT, SEPA, cards, SCA) —
  GDPR-compatible candidates: Stripe, Paddle, Mollie, Adyen, GoCardless,
  Lago, Kill Bill, Chargebee, Payrexx, Lemon Squeezy
- ⬜ Evaluate tracking, logs and statistics — GDPR-compatible candidates:
  Plausible, Matomo, Pirsch, Simple Analytics, Umami, PostHog, Better Stack,
  Grafana Cloud, Sentry, SigNoz
- ⬜ Implement whatever platforms the evaluations chose: login, billing,
  tracking and logs in the app

## Phase 1 — Invoicing ⬜

The reason this repo exists: the invoicing core, extended with its two input
paths.

- ⬜ Port the invoicing core from pocket-cfo (documents, rendering, money)
- ⬜ Milestone path: free text + chat interface; the client's approval is
  recorded in the chat and gates invoice creation
- ⬜ Hourly path: scanned PDF timesheet as the invoice source
- ⬜ Explicit non-goal held: no invoice is ever derived from Toggl data

## Phase 2 — Dashboard ⬜

A central view — a mini CRM for the one freelancer. Built on the invoicing
core's data, and extended as later phases land (the pipeline column fills up
once contract intake exists).

- ⬜ Clients: the list, contact data, the standing of every client at a glance
- ⬜ Earnings: revenue per client, per month, per year — computed on read,
  never stored (see Principles)
- ⬜ Open points: unpaid and overdue invoices, open approvals, drafts waiting
  to be sent
- ⬜ Pipeline: what is coming — contracts in progress, expected volume

## Phase 3 — pocket-cfo integration ⬜

Close the loop back to where invoicing came from.

- ⬜ REST API over the service layer
- ⬜ MCP surface for the agent side, mirroring pocket-cfo's agent-API pattern
- ⬜ Point pocket-cfo at this app and remove/retire its invoicing half

## Phase 4 — Contract intake ⬜

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

## Phase 5 — Tracking (Toggl) ⬜

Where the work under a contract is measured.

- ⬜ Define the tracking-source interface (hours, rates, costs, per project /
  milestone / task)
- ⬜ Toggl implementation behind that interface — the only file allowed to
  know Toggl exists
- ⬜ Standing view: budget used vs. budget available per project and
  milestone, hours spent, where each engagement stands
