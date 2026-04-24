# DevOps CI/CD Microservice on OpenShift (Flask + SQLite + Helm)

This project is a complete DevOps pipeline that deploys a Flask microservice on Red Hat OpenShift using GitHub Actions, Docker, and Helm.

It includes a simple REST API with persistent storage using SQLite (ephemeral file-based storage).

---

## Architecture Flow

```mermaid
flowchart TD
    A[GitHub Push] --> B[GitHub Actions CI/CD]
    B --> C[Docker Build Image]
    C --> D[Docker Hub Push]
    D --> E[OpenShift Deploy via Helm]
    E --> F[Flask App Pod]
    F --> G[SQLite DB file]
    E --> H[OpenShift Route HTTPS]
```

---

## Technologies Used

- Python 3 / Flask
- SQLite (embedded DB)
- Docker
- Kubernetes / OpenShift
- Helm
- GitHub Actions (CI/CD)
- OpenShift Routes (HTTPS ingress)

---

## Project Structure

```
CI-CD-Microservice/
│
├── app/
│   └── app.py
│
├── helm/
│   └── devops-app/
│       ├── templates/
│       ├── values.yaml
│       └── Chart.yaml
│
├── Dockerfile
├── requirements.txt
└── .github/workflows/deploy.yml
```

---

## ⚙️ Features

- REST API built with Flask
- SQLite database (no external DB required)
- CRUD endpoint for tasks
- Health check endpoint
- Containerized with Docker
- Deployed on OpenShift via Helm
- CI/CD pipeline using GitHub Actions

---

## 📡 API Endpoints

### Health check
```
GET /health
```

Response:
```json
{"status": "ok"}
```

---

### Create task
```
POST /tasks
```

Body:
```json
{
  "name": "my task"
}
```

---

### Get tasks
```
GET /tasks
```

Response:
```json
[
  [1, "task 1"],
  [2, "task 2"]
]
```

---

## Deployment Flow

1. Push code to `main`
2. GitHub Actions builds Docker image
3. Image is pushed to Docker Hub
4. Helm deploys to OpenShift
5. Route exposes the service via HTTPS

---

## OpenShift Notes

This project is designed for Red Hat OpenShift sandbox environments:

- Uses OpenShift Routes for HTTPS exposure
- Compatible with restricted security context
- SQLite runs in ephemeral storage (`/tmp`)

---

## Limitations

- SQLite is not suitable for multi-replica deployments
- Data is not persistent across pod restarts (unless volume is added)
- Designed for learning and DevOps demonstration purposes

---

## Possible Improvements

- Add persistent volume for SQLite
- Replace SQLite with PostgreSQL (production version)
- Add frontend dashboard (React or simple HTML)
- Improve API response formatting (JSON objects)
- Add observability (logs, metrics)

---

## Author

DevOps learning project for CI/CD, Kubernetes, and OpenShift practice.

---
