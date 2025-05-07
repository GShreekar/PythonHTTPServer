import socket
import argparse
import os
import threading

def responseMessage(request):
    status = request.splitlines()[0]
    parts = status.split()
    if len(parts) >= 2:
        path = parts[1]
    else:
        path = ""
    method = parts[0]
    if method == "GET":
        if path == "/":
            return "HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo/"):
            content = path[6:]
            return (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(content)}\r\n"
                f"\r\n"
                f"{content}"
            )
        elif path == "/user-agent":
            userAgent = request.split("User-Agent: ")[1].split("\r\n")[0]
            return (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(userAgent)}\r\n"
                f"\r\n"
                f"{userAgent}"
            )
        elif path.startswith("/files/"):
            file = path[7:]
            if os.path.isfile(file):
                with open(file, 'rb') as f:
                    content = f.read()
                return (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    f"\r\n"
                    f"{content.decode()}"
                )
            else:
                return "HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    elif method == "POST":
        if path.startswith("/files/"):
            file = path[7:]
            content = request.split("\r\n\r\n")[1]
            with open(file, 'wb') as f:
                f.write(content.encode())
            return "HTTP/1.1 201 Created\r\n\r\n"
        else:
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    
def handle_client(connection):
    request = connection.recv(1024).decode()
    print(request)
    response = responseMessage(request)
    connection.sendall(response.encode())
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--directory', type=str, help='Directory to serve files from',
        required=False
    )
    args = parser.parse_args()
    root = args.directory
    if root:
        print(f"Serving files from {root}")
        try:
            os.chdir(root)
        except FileNotFoundError:
            print(f"Directory {root} not found.")
            exit(1)
    else:
        print("No directory specified. Using current directory.")
    serverSocket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, _ = serverSocket.accept()
        thread = threading.Thread(target=lambda: handle_client(connection))
        thread.start()
