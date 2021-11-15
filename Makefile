test:
	docker-compose run backend pytest

run_all:
	docker-compose up

run_db:
	docker-compose up db

run_backend:
	docker-compose up backend

network:
	docker network create external-network

swapi:
	scripts/install_swapi.sh
