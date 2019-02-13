import socket
import sys

#define server address, create socket, bind, and listen
server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

try:
    while True:
        client_socket, client_address = server_socket.accept()

        # receive data from client and print
        data = client_socket.recv(1024)
        operasi = data.split(' ')
        if operasi[1] == '+' :
            print int(operasi[0]) + int(operasi[2])
        elif operasi[1] == '-' :
            print int(operasi[0]) - int(operasi[2])
        elif operasi[1] == '*' :
            print int(operasi[0]) * int(operasi[2])
        elif operasi[1] == '/' :
            print int(operasi[0]) / int(operasi[2])
        

        # close socket client
        client_socket.close()

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)