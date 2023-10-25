.PHONY:install
install :
	poetry install 

.PHONY:migrate
migrate:
	poetry run python manage.py migrate

.PHONY:migrations
migrations:
	poetry run python manage.py makemigrations

.PHONY:runserver
runserver:
	poetry run python manage.py runserver

.PHONY:superuser
superuser:
	poetry run python manage.py createsuperuser

.PHONY:collecstatic
collecstatic:
	poetry run python manage.py collecstatic
