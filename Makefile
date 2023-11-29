UID := $(shell id -u)
export UID

.PHONY: d-dev-i-run
# Make all actions needed for run homework from zero.
d-dev-i-run:
	@make init-configs &&\
	make d-run


.PHONY: d-dev-i-purge
# Make all actions needed for purge homework related data.
d-dev-i-purge:
	@make d-purge


.PHONY: init-configs
# Configuration files initialization
init-configs:
	@bash docker/app/init-configs.sh


.PHONY: d-run
# Just run
d-run:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=full_dev \
		docker compose \
			up --build


.PHONY: d-run-i-local-dev
# Just run
d-run-i-local-dev:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=local_dev \
		docker compose \
			up --build


.PHONY: d-purge
# Purge all data related with services
d-purge:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=full_dev \
		docker compose down --volumes --remove-orphans --rmi local --timeout 0


.PHONY: init-dev
# Init environment for development
init-dev:
	@pip install --upgrade pip && \
	pip install --requirement requirements/local.txt && \
	pre-commit install


# [pre-commit]-[BEGIN]
.PHONY: pre-commit-run
# Run tools for files from commit.
pre-commit-run:
	@pre-commit run

.PHONY: pre-commit-run-all
# Run tools for all files.
pre-commit-run-all:
	@pre-commit run --all-files
# [pre-commit]-[END]


.PHONY: migrations
# Make migrations
migrations:
	@python manage.py makemigrations

.PHONY: migrate
# Migrate
migrate:
	@python manage.py migrate


.PHONY: init-dev-i-create-superuser
# Create superuser only for development
init-dev-i-create-superuser:
	@python manage.py createsuperuser --no-input

