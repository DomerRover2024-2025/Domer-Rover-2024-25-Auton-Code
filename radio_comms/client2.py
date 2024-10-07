import socket

# change to IP-address of the computer you are trying to connect to
# if you want to connect to your own computer, leave as is
#host = "169.254.84.229" #socket.gethostname()

host = "10.7.90.102"

port = 12345

client_socket = socket.socket()

client_socket.connect((host, port))

while True:
    message = input("enter message: ")
    if message == "quit":
        break
    encoded = message.encode()
    client_socket.send(encoded)
client_socket.close()