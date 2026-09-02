# Cloud-Native Delivery Platform

![CI](https://github.com/husseinrabeeah/cloud-native-delivery-platform/actions/workflows/ci.yml/badge.svg)

A containerised REST API for normalising rule strings (e.g. firewall rules, config entries, policy statements), built as a hands-on exercise in production-grade Docker practices and cloud deployment.

## Why this project exists

I built this as part of a structured DevOps learning path (Git → Linux → Networking → Docker → Kubernetes → Terraform → Cloud), currently working through end-to-end containerisation and deployment. The goal was to go beyond a toy "hello world" container and practise the patterns actually used in production: multi-stage builds, non-root execution, health checks, and a real deployment pipeline — not just `docker run` on a laptop.

## What it does

The API exposes three endpoints:

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/` | Service status check |
| `GET` | `/health` | Health check (used by Docker/host health probes) |
| `POST` | `/normalise` | Accepts a `rule` string and returns it lowercased with whitespace collapsed |

**Example:**

```bash
curl -X POST https://cloud-native-delivery-platform.onrender.com
  -H "Content-Type: application/json" \
  -d '{"rule": "  DROP  ALL   TRAFFIC  "}'
```

```json
{
  "original": "  DROP  ALL   TRAFFIC  ",
  "normalised": "drop all traffic"
}
```

## Architecture

- **Flask** — application framework, structured with an app factory (`create_app()`) rather than a bare module-level app, for testability
- **Gunicorn** — production WSGI server (not Flask's dev server)
- **Docker** — multi-stage build: a `builder` stage installs dependencies into a virtual environment, and a separate `runtime` stage copies only the built venv and app code, keeping the final image lean
- **Non-root container user** — the app runs as an unprivileged `appuser`, not root, inside the container
- **Health check** — a `HEALTHCHECK` instruction polls `/health` on an interval so the container runtime can detect and react to a hung process
- **Deployment** — [Render](https://render.com), deployed directly from this repository via its Dockerfile

## Running locally

```bash
# Clone and enter the repo
git clone https://github.com/husseinrabeeah/cloud-native-delivery-platform.git
cd cloud-native-delivery-platform

# Build and run with Docker
docker build -t cloud-native-delivery-platform .
docker run -p 8000:8000 cloud-native-delivery-platform
```

The API will be available at `http://localhost:8000`.

## Running tests

```bash
pip install -r requirements.txt
pytest
```

## What's next

This project is a live work-in-progress, evolving alongside my DevOps learning path:

- [ ] CI pipeline (GitHub Actions) to run tests and build the image on every push
- [ ] Kubernetes manifests / Helm chart as a learning exercise once I reach that stage
- [ ] Infrastructure-as-code (Terraform) to provision the deployment target
- [ ] Azure migration once the project is stable (currently on Render's free tier to avoid cloud spend during active development)

## Stack

`Python` · `Flask` · `Gunicorn` · `Docker` · `pytest` · `Render`
