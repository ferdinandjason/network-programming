import socket
import sys

# create socket and connet to server
server_address = ('localhost', 5000)

try :
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        string_matematika = raw_input('Masukkan operasi matematika sederhana : ')
        client_socket.send(string_matematika)
        client_socket.close()

except KeyboardInterrupt:
    sys.exit(0)