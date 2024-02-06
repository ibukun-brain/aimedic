backup_path = "aimedic/.fixtures/backup.json"
branch_name = $$(git branch --show-current)
changed_files = $$(git ls-files '*.py')
os_type = $$(uname -sr)
proj_name = aimedic

all: help
checks: lint test
install: update

# activate:
# 	case $(os_type) in "Darwin*"
# 		@echo 'Mac OS X';;
# 	esac

backup:
	mkdir -p aimedic/.fixtures
	python -Xutf8 manage.py dumpdata \
		--natural-primary \
		--exclude=contenttypes \
		--exclude=auth.permission \
		--exclude=admin.logentry \
		--exclude=sessions.session > $(backup_path)
	echo $(backup_path)

env:
	python -m venv env

fixdb:
	make backup
	rm aimedic.db
	make migrate
	make restore

help:
	@echo
	@echo "Usage: make [commands] e.g. make backup"
	@echo "* backup  | Export database content as json for backup purposes"
	@echo "* env     | Creates a virtual environment in current working directory"
	@echo "* fixdb   | Fixes your database if it gets corrupted. Creates a backup and also restore current data"
	@echo "* help    | Displays this help text"
	@echo "* install | Syncs the project dependencies"
	@echo "* lint    | Checks if code is conforming to best practices like PEP8"
	@echo "* migrate | Runs makemigrations and migrate commands"
	@echo "* push    | Pushes committed changes to the Gitlab remote repository"
	@echo "* restore | Loads previously backed up data into the database"
	@echo "* server  | Spawns the Django server"
	@echo "* test    | Runs unit test"
	@echo "* update  | Syncs the project dependencies"

lint:
	pylint $(changed_files)
	flake8 .
	
fixlint:
	black --check .
	black .
	isort .

migrate:
	python manage.py makemigrations
	python manage.py migrate

push:
	git pull
	git push -u origin $(branch_name)

restore:
	python manage.py loaddata $(backup_path)

server:
	python manage.py runserver 0.0.0.0:8000

server-https:
	python manage.py runserver_plus --cert-file cert.crt

test:
	python manage.py test -v 2 --keepdb

update:
	pip install -r requirements-dev.txt

graph:
	python manage.py graph_models --pydot -a -g -o aimedic-design.png

beat:
	celery -A $(proj_name) beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

worker:
	celery -A $(proj_name) worker -l info --concurrency 1 -P solo

flower:
	celery -A ${proj_name} flower

qcluster:
	python manage.py qcluster

qmonitor:
	python manage.py qmonitor