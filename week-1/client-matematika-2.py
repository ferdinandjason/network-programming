import socket
import sys

# create socket and connet to server
server_address = ('localhost', 5000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try :
    while True:
        string_matematika = raw_input('Operasi matematika : ')
        client_socket.send(string_matematika)
        balasan = client_socket.recv(1024)
        
        print(balasan)

except KeyboardInterrupt:
    sys.exit(0)
    client_socket.close()