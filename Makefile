SHELL := /bin/bash

.PHONY: download-gnaf
download-gnaf:
	@server/scripts/download-gnaf.sh

.PHONY: install
install:
	@cd server &&\
	python3 -m venv venv &&\
	source venv/bin/activate &&\
	pip3 install -r requirements.txt &&\
	python3 scripts/build_gnaf.py

.PHONY: up
up:
	@npm start --prefix client &\
	npm run watch --prefix server &\
	cd server && docker-compose up -d

.PHONY: down
down:
	@cd server && docker-compose down

.PHONY: cp-cert
cp-cert:
	@CONTAINER_NAME=$$(docker ps --format "{{.Names}}" | grep elasticsearch) &&\
	docker cp $$CONTAINER_NAME:/usr/share/elasticsearch/config/certs/ca/ca.crt server/

.PHONY: load-elastic
load-elastic:
	@cd server &&\
	source venv/bin/activate &&\
	python3 scripts/load_elasticsearch.py

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
