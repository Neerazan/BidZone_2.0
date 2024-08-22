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


.PHONY: app
app:
	@echo -e '\033[32mCreating new app...\033[0m'
	cd src && python manage.py startapp $(name);
	@echo -e '\033[32m${name}\033[0m app created successfully inside \033[31m/src/\033[0m directory...'
