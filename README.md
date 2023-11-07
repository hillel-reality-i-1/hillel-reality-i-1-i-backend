# Hillel Reality. 1. Backend.

---
## 🏠 Main development

Development related actions.

### ▶️ Run

Make all actions needed for run Development from zero. Including configuration.

```shell
make d-dev-i-run
```

### 🚮 Purge

Make all actions needed for run Development from zero.

```shell
make d-homework-i-purge
```

---

## 🛠️ Dev

### Initialize dev

Install dependencies and register pre-commit.

```shell
make init-dev
```

### ⚙️ Configure

Configure project.

```shell
make init-configs
```

Change these files if needed:
- [.env](.env)
- [docker-compose.override.yml](docker-compose.override.yml)


### ▶️ Partial run

You can start some services (DB, etc.) in docker and some in local machine (django app, etc.).

Run DB and related services in docker:
```shell
make d-run-i-local-dev
```

Run "django app" on local machine:

Use "Run configuration" (better in Debug mode) in PyCharm:
- "Run django"

---

## 🐳 Docker

Use services in dockers.

### ▶️ Run

Just run

```shell
make d-run
```

### ⏹️Stop

Stop services

```shell
make d-stop
```

### 🚮 Purge

Purge all data related to services

```shell
make d-purge
```

