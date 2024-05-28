#!/usr/bin/env bash

set -euo pipefail

echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
docker build -t iamprithaj/prithaj-portfolio .
docker push iamprithaj/prithaj-portfolio