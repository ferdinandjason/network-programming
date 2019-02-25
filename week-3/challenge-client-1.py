import socket
import sys

server_address = ('127.0.0.1',5002)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
	while True:
		message = sys.stdin.readline()
		client_socket.send(message)
		sys.stdout.write(client_socket.recv(1024))
		sys.stdout.write('>> ')

except KeyboardInterrupt:
	client_socket.close()
	sys.exit()
