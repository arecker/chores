#!/usr/bin/env bash

set -e

PLATFORMS="linux/386,linux/amd64,linux/arm/v7"

docker buildx build \
       --platform "${PLATFORMS}" \
       --output "type=image,push=true" \
       --tag "arecker/chores:latest" \
       --file "Dockerfile" .
