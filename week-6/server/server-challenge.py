import socket

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

file_access = {}
file_name = {}


def send_file(filename, server_socket, client_addresss):
    server_socket.sendto(
        'FILE|'+str(client_addresss[1])+'_'+filename+'|', client_addresss)
    with open(filename, 'r') as f:
        server_socket.sendto(f.read(1024), client_addresss)
    file_name[filename] = str(client_addresss[1])+'_'+filename


while True:
    data, client_addresss = server_socket.recvfrom(1024)
    data = data.split(' ')
    if data[0] == 'DOWNLOAD':
        if data[1] not in file_access:
            send_file(data[1], server_socket, client_addresss)
            file_access[data[1]] = client_addresss
        else:
            server_socket.sendto(
                'COMMAND|'+file_name[data[1]]+'|'+client_addresss[0]+'|'+str(client_addresss[1]), file_access[data[1]])
