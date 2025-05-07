#!/bin/bash

handle_error() {
    echo "Error: $1"
    exit 1
}

if ! command -v pipenv &> /dev/null; then
    handle_error "pipenv could not be found"
fi

echo "Installing dependencies..."
pipenv install || handle_error "Failed to install dependencies"

echo "Starting HTTP server..."
pipenv run python main/main.py "$@"

exit 0