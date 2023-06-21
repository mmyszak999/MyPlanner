build:
		docker-compose build

up:		
		docker-compose up	

migrations:
		docker-compose exec web bash -c "python3 manage.py makemigrations api && python3 manage.py migrate"

superuser:
		docker-compose exec web bash -c "python3 manage.py createsuperuser"

test:
		docker-compose exec web bash -c "python manage.py test"

backend-bash:
		docker-compose exec -it web bash