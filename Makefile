
.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	docker-compose up -V -d

.PHONY: migrate
migrate:
	docker build ./mongo -f mongo/Dockerfile.migrate -t mongo_migrate
	docker run -it --network joker_network mongo_migrate

.PHONY: harvest
harvest:
	docker build ./harvest -f harvest/Dockerfile.harvest -t harvest_info
	docker run -it --network joker_network harvest_info