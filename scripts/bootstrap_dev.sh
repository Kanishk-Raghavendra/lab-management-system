#!/usr/bin/env bash
# Bootstrap developer environment: install python packages, apply DB SQL, start Flask app
# Run this from the project root: bash scripts/bootstrap_dev.sh
set -e

# 1) Install Python requirements (user-local install)
if command -v pip3 >/dev/null 2>&1; then
  echo "Installing Python requirements..."
  pip3 install --user -r requirements.txt
else
  echo "pip3 not found. Please install Python3 and pip before running this script."
  exit 1
fi

# 2) Apply SQL files
echo "Applying SQL files..."
python3 scripts/apply_sql.py

# 3) Start Flask app in background
echo "Starting Flask app (background)..."
python3 run.py &

echo "Bootstrap complete. Flask started in background. Check logs above or use 'ps aux | grep run.py' to verify." 
