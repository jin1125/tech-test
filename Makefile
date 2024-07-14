black:
	docker compose exec app black .

isort:
	docker compose exec app isort .

flake8:
	docker compose exec app flake8 .

mypy:
		docker compose exec app mypy .

format:
	docker compose exec app black .
	docker compose exec app isort .

check:
	docker compose exec app black . --check
	docker compose exec app isort . --check-only
	docker compose exec app flake8 .
	docker compose exec app mypy .

test:
	docker compose exec app pytest $(LIBRARY) ./tests

poetry_show:
	docker compose exec app poetry show

poetry_add:
	docker compose exec app poetry add $(LIBRARY)

poetry_add_dev:
	docker compose exec app poetry add -G dev $(LIBRARY)

poetry_remove:
	docker compose exec app poetry remove $(LIBRARY)

poetry_update:
	docker compose exec app poetry update

migrate:
	alembic revision --autogenerate

db_upgrade:
	alembic upgrade head

db_downgrade:
	alembic downgrade -1
