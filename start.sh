#!/bin/bash
set -e

echo -e "\n\n-------------------------------------------------------------------------------------------" >> artifacts/app.log
echo "$(date +"%Y-%m-%d %H:%M:%S")" >> artifacts/app.log

python3 main.py >> artifacts/app.log