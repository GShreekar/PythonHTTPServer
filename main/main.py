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
            request = request.splitlines()[0]
            parts = request.split()
            if len(parts) >= 2:
                path = parts[1]
            else:
                path = ""
            if path == "/":
                connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")



if __name__ == "__main__":
    main()
