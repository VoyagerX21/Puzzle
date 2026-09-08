# ==============================================================================
# Makefile for Django 8-Puzzle Game Docker Management
# ==============================================================================

# Variables (override via command line: make build IMAGE_NAME=myuser/puzzle TAG=v1)
IMAGE_NAME ?= voyagerx21/puzzle-game
TAG        ?= latest
PORT       ?= 8080
CONTAINER  ?= puzzle_web

.PHONY: help build build-nc push run stop restart logs shell up down compose-logs test clean

# Default target: show help
help:
	@echo "======================================================================"
	@echo "  Django 8-Puzzle — Docker Commands Makefile"
	@echo "======================================================================"
	@echo "  make build         - Build Docker image ($(IMAGE_NAME):$(TAG))"
	@echo "  make build-nc      - Build Docker image without cache"
	@echo "  make push          - Push Docker image to Docker Hub"
	@echo "  make run           - Run container in background on port $(PORT)"
	@echo "  make stop          - Stop and remove running container"
	@echo "  make restart       - Restart container (stop + run)"
	@echo "  make logs          - Follow live container logs"
	@echo "  make shell         - Open interactive shell inside running container"
	@echo "  make up            - Start services using Docker Compose"
	@echo "  make down          - Stop services using Docker Compose"
	@echo "  make compose-logs  - Follow Docker Compose service logs"
	@echo "  make test          - Run Django unit tests inside Docker container"
	@echo "  make clean         - Prune dangling images and stopped containers"
	@echo "======================================================================"

# Build Docker image
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Build Docker image without cache
build-nc:
	docker build --no-cache -t $(IMAGE_NAME):$(TAG) .

# Push image to Docker Hub
push:
	docker push $(IMAGE_NAME):$(TAG)

# Run container standalone on port 8080 with persistent volume
run: stop
	docker run -d \
		--name $(CONTAINER) \
		--restart unless-stopped \
		-p $(PORT):8080 \
		-e PORT=8080 \
		-e DEBUG=False \
		-e ALLOWED_HOSTS="*" \
		-v puzzle_media:/app/media \
		-v puzzle_db:/app/data \
		$(IMAGE_NAME):$(TAG)
	@echo "Container $(CONTAINER) started on http://localhost:$(PORT)"

# Stop and remove container if running
stop:
	@docker stop $(CONTAINER) 2>/dev/null || true
	@docker rm $(CONTAINER) 2>/dev/null || true

# Restart standalone container
restart: stop run

# View live container logs
logs:
	docker logs -f $(CONTAINER)

# Open interactive shell in container
shell:
	docker exec -it $(CONTAINER) sh

# Docker Compose: start in background
up:
	docker compose up -d

# Docker Compose: stop services
down:
	docker compose down

# Docker Compose: follow logs
compose-logs:
	docker compose logs -f

# Run automated tests in a temporary container
test:
	docker run --rm $(IMAGE_NAME):$(TAG) python manage.py test

# Clean up dangling images
clean:
	docker container prune -f
	docker image prune -f
