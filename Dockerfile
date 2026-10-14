ARG GO_VERSION=1
FROM golang:${GO_VERSION}-bookworm as builder

WORKDIR /usr/src/app
COPY go.mod ./
RUN go mod download && go mod verify
COPY . .
RUN CGO_ENABLED=0 go build -o /out/freelancer-invoicing .

FROM debian:bookworm as runtime
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /out/freelancer-invoicing /usr/local/bin/freelancer-invoicing

CMD ["freelancer-invoicing"]
