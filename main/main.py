import socket
import argparse
import os
import threading

def responseMessage(request):
    try:
        status = request.splitlines()[0]
        parts = status.split()
        if len(parts) >= 2:
            path = parts[1]
        else:
            path = ""
        method = parts[0]

        if method == "GET":
            if path == "/":
                return "HTTP/1.1 200 OK\r\n\r\n".encode()
            elif path.startswith("/echo/"):
                content = path[6:]
                encodings = []
                if "Accept-Encoding: " in request:
                    encodings = request.split("Accept-Encoding: ")[1].split("\r\n")[0].split(", ")
                if encodings and "gzip" in encodings:
                    import gzip
                    content = gzip.compress(content.encode())
                    return (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: text/plain\r\n"
                        f"Content-Encoding: gzip\r\n"
                        f"Content-Length: {len(content)}\r\n"
                        f"\r\n"
                    ).encode() + content
                else:
                    return (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: text/plain\r\n"
                        f"Content-Length: {len(content)}\r\n"
                        f"\r\n"
                        f"{content}"
                    ).encode()
            elif path == "/user-agent":
                if "User-Agent: " in request:
                    userAgent = request.split("User-Agent: ")[1].split("\r\n")[0]
                else:
                    userAgent = "Unknown"
                return (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(userAgent)}\r\n"
                    f"\r\n"
                    f"{userAgent}"
                ).encode()
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
                    ).encode() + content
                else:
                    return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        elif method == "POST":
            if path.startswith("/files/"):
                file = path[7:]
                content = request.split("\r\n\r\n", 1)[1].encode()  # Handle raw bytes
                with open(file, 'wb') as f:
                    f.write(content)
                return "HTTP/1.1 201 Created\r\n\r\n".encode()
            else:
                return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            return "HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode()
    except Exception as e:
        return f"HTTP/1.1 500 Internal Server Error\r\n\r\n{str(e)}".encode()

def handle_client(connection):
    try:
        while True:
            request = connection.recv(1024).decode()
            if not request:
                break
            print(request)
            response = responseMessage(request)
            connection.sendall(response)

            if "Connection: close" in request:
                print("Connection: close header received. Closing connection.")
                break
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
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
        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()
