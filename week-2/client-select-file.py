import socket
import sys

server_address = ('127.0.0.1',5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        filename = sys.stdin.readline()
        filename = filename[:-1]
        with open(filename,'rb') as f:
            chunk = f.read(1024)
            while chunk:
                client_socket.send(chunk)
                chunk = f.read(1024)

        client_socket.send('NAMA:'+filename)
        sys.stdout.write('>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit()
