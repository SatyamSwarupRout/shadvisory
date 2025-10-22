# ==============================================
# FastAPI + PostgreSQL + Alembic Docker Makefile
# ==============================================

# Service names (match docker-compose.yml)
DC          = docker-compose
WEB         = web
DB          = db
ENV_FILE    = .env

# -----------------------------
# 🚀 Containers
# -----------------------------

# Build and start containers in background
up:
	$(DC) up --build

# Stop containers
down:
	$(DC) down

# Show container status
ps:
	$(DC) ps

# View logs for FastAPI container
logs:
	$(DC) logs -f $(WEB)

# Restart only FastAPI container
restart:
	$(DC) restart $(WEB)

# Open interactive shell inside FastAPI container
shell:
	$(DC) exec $(WEB) /bin/bash

# -----------------------------
# 🗄️ Database & Alembic
# -----------------------------

# Create a new migration (use: make revision msg="add users table")
revision:
	$(DC) run --rm --env-file $(ENV_FILE) $(WEB) alembic revision --autogenerate -m "$(msg)"

# Apply latest migrations
migrate:
	$(DC) run --rm --env-from-file $(ENV_FILE) $(WEB) alembic upgrade head

# Roll back one migration
downgrade:
	$(DC) run --rm --env-from-file $(ENV_FILE) $(WEB) alembic downgrade -1

# Show migration history
history:
	$(DC) run --rm --env-file $(ENV_FILE) $(WEB) alembic history

# Recreate database schema from scratch
reset-db:
	$(DC) run --rm $(WEB) alembic downgrade base
	$(DC) run --rm $(WEB) alembic upgrade head

# -----------------------------
# 🧹 Utilities
# -----------------------------

# Tail Postgres logs
dblogs:
	$(DC) logs -f $(DB)

# Clean all containers, volumes, and networks
clean:
	$(DC) down -v --remove-orphans
