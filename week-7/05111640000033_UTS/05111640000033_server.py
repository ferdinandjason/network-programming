import socket
import sys
import os

from thread import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_ADDRESS = '127.0.0.1'
PORT = 8801
MAX_BUFFER = 2048

server_socket.bind((IP_ADDRESS, PORT))
server_socket.listen(100)

list_of_clients = []

TYPE_FILE = 'FILE'
TYPE_MESSAGE = 'MESG'
TYPE_END = 'EOF'
TYPE_SEND = 'SEND'
TYPE_UPLOAD = 'UPLD'
TYPE_LIST = 'LIST'
TYPE_SENDALL = 'SDAL'
TYPE_DOWNLOAD = 'DOWN'
TYPE_REMOVE = 'DELL'

PATH_SERVER = './file-server/'

if not os.path.exists(PATH_SERVER):
    os.mkdir(PATH_SERVER)


def client_thread(connection, address):
    while True:
        message = connection.recv(MAX_BUFFER)
        if message:
            TYPE = message[:4]
            if TYPE == TYPE_UPLOAD:
                chunk = message.split('|')
                print chunk
                if len(chunk) == 2:
                    filename = chunk[0][5:]
                    chunk = chunk[1]
                else:
                    filename = chunk[0][5:]
                    chunk = ''
                print PATH_SERVER+filename
                with open(PATH_SERVER+filename, 'wb') as f:
                    lanjut = True
                    f.write(chunk)
                    if TYPE_END in chunk:
                        chunk = chunk.replace(TYPE_END, '')
                        f.write(chunk)
                        lanjut = False
                    while lanjut:
                        chunk = connection.recv(MAX_BUFFER)
                        if TYPE_END in chunk:
                            chunk = chunk.replace(TYPE_END, '')
                            f.write(chunk)
                            break
                        f.write(chunk)
                connection.send(TYPE_UPLOAD+':File uploaded!')
            elif TYPE == TYPE_LIST:
                list_file = os.popen("ls "+PATH_SERVER).read()
                connection.send(TYPE_LIST+':'+list_file)
            elif TYPE == TYPE_SENDALL:
                chunk = message.split('|')
                print chunk
                if len(chunk) == 2:
                    filename = chunk[0][5:]
                    chunk = chunk[1]
                else:
                    filename = chunk[0][5:]
                    chunk = ''
                print PATH_SERVER+filename
                with open(PATH_SERVER+filename, 'wb') as f:
                    lanjut = True
                    f.write(chunk)
                    if TYPE_END in chunk:
                        chunk = chunk.replace(TYPE_END, '')
                        f.write(chunk)
                        lanjut = False
                    while lanjut:
                        chunk = connection.recv(MAX_BUFFER)
                        if TYPE_END in chunk:
                            chunk = chunk.replace(TYPE_END, '')
                            f.write(chunk)
                            break
                        f.write(chunk)
                broadcast_file(PATH_SERVER+filename, connection)
            elif TYPE == TYPE_DOWNLOAD:
                filename = message[5:]
                with open(PATH_SERVER+filename, 'rb') as f:
                    filename_new = filename.replace(PATH_SERVER, '')
                    try:
                        connection.send(TYPE_FILE+':'+filename_new+'|')
                        chunk = f.read(MAX_BUFFER)
                        while chunk:
                            connection.send(chunk)
                            chunk = f.read(MAX_BUFFER)
                        connection.send(TYPE_END)
                    except:
                        connection.close()
                        remove_from_list(connection)
            elif TYPE == TYPE_REMOVE:
                os.remove(PATH_SERVER+message[5:])
                connection.send(TYPE_REMOVE+':File Removed')
            elif TYPE == TYPE_MESSAGE:
                message_to_send = "<" + address[0] + "> : " + message[5:]
                print message_to_send
                broadcast_mesg(message_to_send, connection)
        else:
            remove_from_list(connection)


def broadcast_file(filename, connection):
    for client in list_of_clients:
        if client != connection:
            print filename
            with open(filename, 'rb') as f:
                filename_new = filename.replace(PATH_SERVER, '')
                try:
                    client.send(TYPE_FILE+':'+filename_new+'|')
                    chunk = f.read(MAX_BUFFER)
                    while chunk:
                        client.send(chunk)
                        chunk = f.read(MAX_BUFFER)
                    client.send(TYPE_END)
                except:
                    client.close()
                    remove_from_list(client)


def broadcast_mesg(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(TYPE_MESSAGE+":"+message)
            except:
                client.close()
                remove_from_list(client)


def remove_from_list(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    connection, address = server_socket.accept()
    list_of_clients.append(connection)
    print address[0] + ':' + str(address[1]) + ' connected'
    start_new_thread(client_thread, (connection, address))

connection.close()
server_socket.close()
