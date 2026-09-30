#!/bin/bash

docker rm -f bmetaap 2>/dev/null || true

docker build -t bmetimg .

docker run --rm --name bmetaap -p 3000:3000 -v $(pwd):/bmeta bmetimg