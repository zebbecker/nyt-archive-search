#!/bin/bash
set -e 

export SERVER=159.203.178.166

# Deploy Django project
./scripts/upload-code.sh
./scripts/install-code.sh

