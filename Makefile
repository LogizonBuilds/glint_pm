.PHONY: run
run:
	@python manage.py runserver $(port)

install:
	@pip install $(package)

csu:
	@python manage.py createsuperuser

mms:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

shell:
	@python manage.py shell

dbshell:
	@python manage.py dbshell

test:
	@pytest

celery-default:
	@celery -A glint_pm.celery worker --loglevel=INFO --concurrency 1 -P solo