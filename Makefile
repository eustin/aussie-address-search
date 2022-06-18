SHELL := /bin/bash

.PHONY: install
install:
	@./scripts/download-gnaf.sh

.PHONY: up
up:
	docker-compose up

.PHONY: up-d
up-d:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down
