import socket
import select
import sys
import os
import random
import string

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_ADDRESS = '127.0.0.1'
PORT = 8801
MAX_BUFFER = 2048

TYPE_FILE = 'FILE'
TYPE_MESSAGE = 'MESG'
TYPE_END = 'EOF'
TYPE_SEND = 'SEND'
TYPE_UPLOAD = 'UPLD'
TYPE_LIST = 'LIST'
TYPE_SENDALL = 'SDAL'
TYPE_DOWNLOAD = 'DOWN'
TYPE_REMOVE = 'DELL'

PATH_CLIENT = './file-client/'

if not os.path.exists(PATH_CLIENT):
    os.mkdir(PATH_CLIENT)

server_socket.connect((IP_ADDRESS, PORT))

while True:
    hash_random = hash = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    socket_list = [sys.stdin, server_socket]
    read_socket, write_socket, error_socket = select.select(socket_list, [], [])

    for socket in read_socket:
        if socket == server_socket:
            message = socket.recv(MAX_BUFFER)
            TYPE = message[:4]
            if TYPE == TYPE_UPLOAD:
                message = message[5:]
                print message
            elif TYPE == TYPE_LIST:
                message = message[5:]
                print message
            elif TYPE == TYPE_FILE:
                chunk = message.split('|')
                if len(chunk) == 2:
                    filename = chunk[0][5:]
                    chunk = chunk[1]
                else :
                    chunk = ''
                    filename = chunk[0][5:] 
                with open(PATH_CLIENT+hash_random+'_'+filename, 'wb') as f:
                    lanjut = True
                    f.write(chunk)
                    if TYPE_END in chunk:
                        chunk = chunk.replace(TYPE_END,'')
                        f.write(chunk)
                        lanjut = False
                    while lanjut:
                        chunk = socket.recv(MAX_BUFFER)
                        if TYPE_END in chunk:
                            chunk = chunk.replace(TYPE_END,'')
                            f.write(chunk)
                            break
                        f.write(chunk)
                print 'File received :' + hash_random+'_'+filename
            elif TYPE == TYPE_REMOVE:
                print message[5:]
            elif TYPE == TYPE_MESSAGE:
                print message[5:]
        else :
            message = sys.stdin.readline()
            message = message.strip()
            if message.startswith("UPLOAD"):
                message = message[7:]
                server_socket.send(TYPE_UPLOAD+':'+message+'|')
                with open(PATH_CLIENT+message, 'rb') as f:
                    chunk = f.read(MAX_BUFFER)
                    while chunk:
                        server_socket.send(chunk)
                        chunk = f.read(MAX_BUFFER)
                server_socket.send(TYPE_END)
                sys.stdout.write("<You> : Sending file to server")
                sys.stdout.write("\n")
                sys.stdout.flush()
            elif message.startswith("LIST"):
                message = message[5:]
                server_socket.send(TYPE_LIST)
            elif message.startswith("SENDALL"):
                sys.stdout.write("<You> : Sending file to all client")
                message = message[8:]
                server_socket.send(TYPE_SENDALL+':'+message+'|')
                with open(PATH_CLIENT+message, 'rb') as f:
                    chunk = f.read(MAX_BUFFER)
                    while chunk:
                        server_socket.send(chunk)
                        chunk = f.read(MAX_BUFFER)
                server_socket.send(TYPE_END)
                sys.stdout.write("<You> : ")
                sys.stdout.write("Send file with name "+ message)
                sys.stdout.write("\n")
                sys.stdout.flush()
            elif message.startswith("DOWNLOAD"):
                message = message[9:]
                sys.stdout.write("<You> : Downloading")
                server_socket.send(TYPE_DOWNLOAD+':'+message)
            elif message.startswith("REMOVE"):
                message = message[7:]
                sys.stdout.write("<You> : Remove file")
                server_socket.send(TYPE_REMOVE+':'+message)
            else :
                server_socket.send(TYPE_MESSAGE+':'+message)
                sys.stdout.write("<You> : ")
                sys.stdout.write(message)
                sys.stdout.write("\n")
                sys.stdout.flush()
