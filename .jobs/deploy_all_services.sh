#!/usr/bin/env bash

set -euo pipefail

docker pull prithaj-portfolio
docker stop prithaj-portfolio
docker remove prithaj-portfolio
docker run -d --name prithaj-portfolio -p 80:9000 -e GH_ACCESS_TOKEN=$GH_ACCESS_TOKEN prithaj-portfolio