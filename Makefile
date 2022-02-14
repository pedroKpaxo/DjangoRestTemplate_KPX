ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

up:
	python manage.py runserver

migrations:
	python manage.py makemigrations $(ARG)

migrate:
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell_plus

startapp:
	bash scripts/start-app.sh $(ARG)

setup_common:
	bash scripts/setup-common.sh

setup_venv:
	bash scripts/setup-venv.sh