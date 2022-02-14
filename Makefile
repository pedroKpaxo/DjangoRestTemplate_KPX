ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

up:
	python manage.py runserver

migrations:
	@echo "Running migrations from Makefile"
	python manage.py makemigrations $(ARG)

migrate:
	@echo "Running migrate from Makefile"
	python manage.py migrate

createsuperuser:
	@echo "Creating super user"
	python manage.py createsuperuser

shell:
	@echo "Entering shell from django-extensions"
	python manage.py shell_plus

startapp:
	bash scripts/start-app.sh $(ARG)

setup_common:
	bash scripts/setup-common.sh

setup_venv:
	bash scripts/setup-venv.sh