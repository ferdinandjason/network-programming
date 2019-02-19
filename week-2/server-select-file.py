import socket
import select
import sys
import time
import datetime
import os

server_address = ('127.0.0.1',5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
client_sockets = {}

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket :
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                client_sockets[client_socket] = client_address
            else:
                print('Receiving File ...')
                data = sock.recv(1024)
                with open('temp_'+str(sock.getpeername()[1]),'wb') as f:
                    while True:
                        if(data[:4] == 'NAMA') :
                            break
                        f.write(data)
                        data = sock.recv(1024)
                print('File Received !')
                os.rename('temp_'+str(sock.getpeername()[1]),data[5:]+'_server')


except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)