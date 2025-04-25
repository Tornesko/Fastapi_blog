
# 🚀 FastAPI MVC Blog App

Simple FastAPI application using MVC pattern with authentication, MySQL database, and caching.

---


1. **Clone the repository:**


2. **Build and start the application:**

```bash
make run
```

3. **Initialize the database:**

```bash
make init_db
```

4. **Open API documentation:**

Go to [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠 Available Make Commands

| Command | Description |
|:--------|:------------|
| `make build` | Build Docker containers |
| `make up` | Start containers |
| `make down` | Stop and remove containers and volumes |
| `make restart` | Rebuild and restart everything |
| `make run` | Build and start the app |
| `make init_db` | Initialize the database tables |

