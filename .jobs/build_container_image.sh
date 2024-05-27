#!/usr/bin/env bash

set -euo pipefail

echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
docker build -t prithaj-portfolio .
docker push prithaj-portfolio