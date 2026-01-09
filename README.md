# Todo App Backend

A backend REST API built with **Falcon** and **Pony ORM**.

---

## 🚀 Tech Stack
- Python 3.10.7
- Falcon (Web Framework)
- Pony ORM
- PostgreSQL / MySQL (configurable)

---

## 📦 Requirements
- Python 3.10+
- pip / virtualenv
- Database (PostgreSQL recommended)

---

## ⚙️ Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Run Application (Gunicorn)

This project uses **Gunicorn** as the WSGI HTTP server.

Example:
```
gunicorn app.main:api -w 5 -b 0.0.0.0:8000
```

The API will be available at:
```
http://localhost:8000
```

---

### Swagger UI

Swagger documentation is available at:
```
http://localhost:8000/apidoc/swagger
```
