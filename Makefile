tokenfile := _token
TOKEN :=$(file < $(tokenfile))
versionfile := _version
VERSION :=$(file < $(versionfile))
IMAGE := brokenpip3/rtt
LOCALCONFIG := example-settings.yaml
REMOTECONFIG := /usr/src/app/settings.yaml

.PHONY: all build push docker-run

all: build push docker-run

build:
	docker build -t $(IMAGE):$(VERSION) . --no-cache

push:
	docker push $(IMAGE):$(VERSION)

docker-run:
	docker run -i -t --rm --env-file=${tokenfile} -v ${PWD}/${LOCALCONFIG}:${REMOTECONFIG} $(IMAGE):$(VERSION)
