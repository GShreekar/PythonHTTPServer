# Python HTTP Server

This is a simple HTTP server implemented in Python. It supports basic GET and POST requests and can serve files from a specified directory.

## Features
- Serve files from a specified directory.
- Handle GET requests for:
  - Root (`/`) - Returns a basic HTTP 200 response.
  - Echo (`/echo/<message>`) - Returns the `<message>` in the response body. Supports gzip compression if requested.
  - User-Agent (`/user-agent`) - Returns the `User-Agent` header from the request.
  - Files (`/files/<filename>`) - Serves the specified file if it exists.
- Handle POST requests to upload files to the server (`/files/<filename>`). Creates the file with the provided content.

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
- Use tools like `curl` or to interact with the server.

## Notes
- Ensure the specified directory exists and contains the files you want to serve.
- The server listens on `localhost:4221` by default.
