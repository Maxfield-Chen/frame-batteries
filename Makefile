IMAGE_NAME = mchen/NEW_PROJECT
VERSION = :latest
CONTAINER_OUTPUT_DIR = /app/output
HOST_OUTPUT_DIR = $(PWD)/output

build:
	@docker build . --quiet -t $(IMAGE_NAME)$(VERSION) --target production

build-dev:
	@docker build . --quiet -t $(IMAGE_NAME)-dev$(VERSION) --target development

run:
	@make build && docker run \
	  -v $(HOST_OUTPUT_DIR):$(CONTAINER_OUTPUT_DIR) \
	  $(IMAGE_NAME)

run-info:
	@make build && docker run \
	  -v $(HOST_OUTPUT_DIR):$(CONTAINER_OUTPUT_DIR) \
	  $(IMAGE_NAME)$(VERSION) --log=INFO

run-debug:
	@make build && docker run \
	  -v $(HOST_OUTPUT_DIR):$(CONTAINER_OUTPUT_DIR) \
	  $(IMAGE_NAME)$(VERSION) --log=DEBUG

test:
	@make build-dev && docker run \
	  -v $(HOST_OUTPUT_DIR):$(CONTAINER_OUTPUT_DIR) \
	  $(IMAGE_NAME)-dev$(VERSION)
	
test-interactive:
	@make build-dev && docker run -it --entrypoint /bin/bash \
	  -v $(HOST_OUTPUT_DIR):$(CONTAINER_OUTPUT_DIR) \
	  $(IMAGE_NAME)-dev$(VERSION)