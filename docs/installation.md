# Running the app

The app is one Go binary serving a web UI on port 8080. There are three ways
to run it: with Go directly, with Docker, or on Fly.io.

## Prerequisites

- **Go 1.27+** (for `go run`) — or **Docker**, if you prefer not to install Go
- **flyctl** only if you want to deploy to Fly.io

## Run with Go

```
go run .
```

Then open http://localhost:8080. The port is fixed at 8080 for now.

## Run with Docker

```
docker build -t freelancer-invoicing .
docker run --rm -p 8080:8080 freelancer-invoicing
```

## Deploy to Fly.io

The app lives at `freelancer-invoicing.fly.dev`, region `fra`. It is configured
to run zero machines when idle (`min_machines_running = 0`, auto-stop
enabled): a request wakes the machine, with a cold start of roughly one to two
seconds.

Manual deploy:

```
fly deploy --remote-only
```

Automatic deploy: every push to `main` triggers the deploy workflow in
[.github/workflows/fly-deploy.yml](../.github/workflows/fly-deploy.yml). This
requires a `FLY_API_TOKEN` secret on the GitHub repository (create one with
`fly tokens create -a freelancer-invoicing`).

Releases are handled separately — see
[release-process.md](release-process.md).
