import socket

# create socket and connet to server
server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# send string to server and close socket
client_socket.send('Hi ... ')
client_socket.close()