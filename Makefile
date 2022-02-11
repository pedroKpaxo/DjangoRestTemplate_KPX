ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

up:
	python manage.py runserver

startapp:
	bash scripts/start-app.sh $(ARG)

setup_commom:
	bash scripts/setup-commom.sh

setup_venv:
	bash scripts/setup-venv.sh