SHELL := /bin/bash

.PHONY: download-gnaf
download-gnaf:
	@./scripts/download-gnaf.sh

.PHONY: install
install:
	@python3 -m venv venv &&\
	source venv/bin/activate &&\
	pip3 install -r requirements.txt

.PHONY: up
up:
	docker-compose up

.PHONY: up-d
up-d:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down
