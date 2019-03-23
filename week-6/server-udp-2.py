import random
import socket

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)

while True:
    data, client_addresss = server_socket.recvfrom(1024)

    if random.randint(0, 1):
        server_socket.sendto(data, client_addresss)
        print 'data:', data, ', client address', client_addresss
        print 'sock name', server_socket.getsockname()
    else:
        print 'server is down'
