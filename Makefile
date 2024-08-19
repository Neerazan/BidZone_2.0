.PHONY: install
install:
	@echo "Installing..."
	pipenv install


.PHONY: install-pre-commit
install-pre-commit:
	pipenv run pre-commit uninstall; pipenv run pre-commit install


.PHONY: lint
lint:
	pipenv run pre-commit run --all-files


.PHONY: run
run:
	python -m src.manage runserver


.PHONY: migrate
migrate:
	python -m src.manage migrate


.PHONY: migrations
migrations:
	python -m src.manage makemigrations


.PHONY: shell
shell:
	python -m src.manage shell


.PHONY: superuser
superuser:
	python -m src.manage createsuperuser


.PHONY: update
update: install migrate;
	@echo "Update Completed..."
