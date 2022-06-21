SHELL := /bin/bash

.PHONY: download-gnaf
download-gnaf:
	@./scripts/download-gnaf.sh

.PHONY: install
install:
	@python3 -m venv venv &&\
	source venv/bin/activate &&\
	pip3 install -r requirements.txt &&\
	python3 scripts/build_gnaf.py

.PHONY: up
up:
	@docker-compose up -d

.PHONY: down
down:
	@docker-compose down

.PHONY: cp-cert
cp-cert:
	@CONTAINER_NAME=$$(docker ps --format "{{.Names}}" | grep elasticsearch) &&\
	docker cp $$CONTAINER_NAME:/usr/share/elasticsearch/config/certs/ca/ca.crt .

.PHONY: load-elastic
load-elastic:
	@source venv/bin/activate &&\
	python3 scripts/load_elasticsearch.py
