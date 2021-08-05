
.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	docker-compose up -V

.PHONY: migrate
migrate:
	docker build ./mongo -f mongo/Dockerfile.migrate -t mongo_migrate
	docker run -it --network joker_network mongo_migrate
