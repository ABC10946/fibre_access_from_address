DOCKER_IMAGE = ghcr.io/abc10946/fibre_from_address
DOCKER_IMAGE_TAG = $(shell git describe --tags --always --dirty --abbrev=14)

docker-build:
	docker build -t $(DOCKER_IMAGE):$(DOCKER_IMAGE_TAG) .

docker-push:
	docker push $(DOCKER_IMAGE):$(DOCKER_IMAGE_TAG)

docker-run:
	docker run -p 5000:5000 $(DOCKER_IMAGE):$(DOCKER_IMAGE_TAG)