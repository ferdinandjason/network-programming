import socket
import select
import sys
import time
import datetime

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
                data = sock.recv(1024)
                string = client_sockets[sock][0] + ',' + str(client_sockets[sock][1]) + ',' + str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + ',' + data
                print sock.getpeername(), data
                with open('pesan.log','a') as f:
                    f.write(string)
                if data :
                    sock.send(data)
                else :
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)