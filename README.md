# Python HTTP Server

This is a simple HTTP server implemented in Python. It supports basic GET and POST requests and can serve files from a specified directory.

## Features
- Serve files from a specified directory.
- Handle GET requests for:
  - Root (`/`)
  - Echo (`/echo/<message>`)
  - User-Agent (`/user-agent`)
  - Files (`/files/<filename>`)
- Handle POST requests to upload files to the server (`/files/<filename>`).

## Requirements
- Python 3
- Pipenv for dependency management

## Setup
1. Install dependencies:
   ```bash
   ./PythonHTTPServer.sh
   ```

2. Start the server:
   ```bash
   ./PythonHTTPServer.sh --directory <path_to_directory>
   ```

## Usage
- Access the server at `http://localhost:4221`.
- Use tools like `curl` to interact with the server.
