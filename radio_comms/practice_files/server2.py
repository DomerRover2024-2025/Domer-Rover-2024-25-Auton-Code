import socket

host = "169.254.240.75"
port = 12345

server_socket = socket.socket()
server_socket.bind((host, port))

server_socket.listen(4)
connection, address = server_socket.accept()

print("connection is from " + str(address))

while True:
    data = connection.recv(1024).decode()
    if not data:
        break
    print(data)

connection.close()