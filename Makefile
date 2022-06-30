SHELL := /bin/bash

server/.env:
	@cp server/.env.template server/.env

.PHONY: setup-gnaf
setup-gnaf:
	@chmod +x server/scripts/download-gnaf.sh &&\
	server/scripts/download-gnaf.sh &&\
	cd server &&\
	python3 -m venv venv &&\
	source venv/bin/activate &&\
	pip3 install -r requirements.txt &&\
	python3 scripts/build_gnaf.py

.PHONY: setup-elastic
setup-elastic:
	@cd server &&\
	docker-compose up -d &&\
	CONTAINER_NAME=$$(docker ps --format "{{.Names}}" | grep elasticsearch) &&\
	docker cp $$CONTAINER_NAME:/usr/share/elasticsearch/config/certs/ca/ca.crt . &&\
	source venv/bin/activate &&\
	python3 scripts/load_elasticsearch.py

.PHONY: install
install:
	@npm install --prefix client &&\
	npm install --prefix server

.PHONY: up
up:
	@npm start --prefix client &\
	npm run watch --prefix server &\
	cd server && docker-compose up -d

.PHONY: down
down:
	@cd server && docker-compose down

.PHONY: watch-server
watch-server:
	@npm run watch --prefix server

.PHONY: client
client:
	@npm start --prefix client

.PHONY: pytest
pytest:
	@cd server &&\
	source venv/bin/activate &&\
	python3 -m pytest
