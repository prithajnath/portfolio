#!/usr/bin/env bash

set -euo pipefail

docker pull prithaj-portfolio
docker stop prithaj-portfolio
docker remove prithaj-portfolio
docker run -d --name prithaj-portfolio -p 80:9000 -e GITHUB_ACCESS_TOKEN=$GITHUB_ACCESS_TOKEN prithaj-portfolio