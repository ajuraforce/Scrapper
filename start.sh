#!/bin/bash
# Render startup script for JobRight Scraper

echo "Starting JobRight Production Scraper..."
echo "Python version: $(python --version)"
echo "Installing dependencies..."

pip install -r requirements.txt

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 --timeout 300 --access-logfile - --error-logfile - app:app