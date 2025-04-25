
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --volumes --remove-orphans

restart:
	docker-compose down --volumes --remove-orphans
	docker-compose build
	docker-compose up -d

init_db:
	docker-compose exec fastapi python -m app.init_db

run: build up

bash:
	docker-compose exec fastapi /bin/bash