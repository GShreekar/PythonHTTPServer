import socket

def main():
    serverSocket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, _ = serverSocket.accept()
        with connection:
            print("Connection established")
            data = connection.recv(1024)
            if not data:
                continue
            request = data.decode("utf-8", errors="ignore")
            print("Request:", request)
            status = request.splitlines()[0]
            parts = status.split()
            if len(parts) >= 2:
                path = parts[1]
            else:
                path = ""
            if path == "/":
                connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            elif path.startswith("/echo"):
                content = path[6:]
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    f"\r\n"
                    f"{content}"
                )
                connection.sendall(response.encode("utf-8"))
            elif path == "/user-agent":
                userAgent = request.split("User-Agent: ")[1].split("\r\n")[0]
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(userAgent)}\r\n"
                    f"\r\n"
                    f"{userAgent}"
                )
                connection.sendall(response.encode("utf-8"))
            else:
                connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")



if __name__ == "__main__":
    main()
