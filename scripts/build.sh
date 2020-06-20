#!/usr/bin/env bash

set -e

PLATFORMS="linux/arm/v7"

docker buildx build \
       --platform "${PLATFORMS}" \
       --output "type=image,push=true" \
       --tag "arecker/chores:latest" \
       --file "Dockerfile" .
