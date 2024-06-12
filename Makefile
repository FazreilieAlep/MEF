.PHONY: run-server
run-server:
	uvicorn app.main:app --reload

.PHONY: install
install:
	poetry install

.PHONY: migrations
migrations:
	cd app && alembic revision --autogenerate -m "migrations"

.PHONY: migrate
migrate:
	cd app && alembic upgrade head

.PHONY: migrate-down
migrate-down:
	cd app && alembic downgrade -1