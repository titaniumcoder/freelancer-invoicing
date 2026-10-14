# Running the app

The app is one Go binary serving a web UI on port 8080. Run it with Go
directly or with Docker. Deploying to Fly.io is not part of this document —
that is what the GitHub Actions do on a release tag.

## Prerequisites

- **Go 1.27+** (for `go run`) — or **Docker**, if you prefer not to install Go

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
