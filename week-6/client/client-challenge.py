import socket
import sys
import select

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_file(filename, server_socket, client_addresss):
    server_socket.sendto(
        'FILE|'+str(client_addresss[1])+'_'+filename+'|', client_addresss)
    with open(filename, 'r') as f:
        server_socket.sendto(f.read(1024), client_addresss)


while True:
    socket_list = [sys.stdin, client_socket]
    read_socket, write_socket, error_socket = select.select(
        socket_list, [], [])

    for socket in read_socket:
        if socket == client_socket:
            recv_message, server_address = client_socket.recvfrom(1024)
            recv_message = recv_message.split('|')
            if recv_message[0] == 'FILE':
                print recv_message
                with open(recv_message[1], 'w') as f:
                    recv_message, server_address = client_socket.recvfrom(1024)
                    f.write(recv_message)
                    print 'file received from', str(server_address)
            else:
                send_file(recv_message[1], client_socket,
                          (recv_message[2], int(recv_message[3])))
        else:
            message = sys.stdin.readline()
            message = message[:-1]
            client_socket.sendto(message, server_address)
