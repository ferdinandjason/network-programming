import socket
import sys

#define server address, create socket, bind, and listen
server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

client_list = []
client_socket_list = []

total_res = 0

string_list = []

try:
    while True:
        client_socket, client_address = server_socket.accept()
        if client_address not in client_list :
            client_list.append(client_address)
            client_socket_list.append(client_socket)

        # receive data from client and print
        data = client_socket.recv(1024)
        print data
        if data == 'END' :
            for client_address, client_socket in zip(client_list, client_socket_list) :
                try:
                    client_socket.send('TOTAL AKHIR : ' + str(total_res) + ' END')
                except:
                    pass
        else : 
            operasi = data.split(' ')
            result = 0
            if operasi[1] == '+' :
                result = int(operasi[0]) + int(operasi[2])
            elif operasi[1] == '-' :
                result = int(operasi[0]) - int(operasi[2])
            elif operasi[1] == '*' :
                result = int(operasi[0]) * int(operasi[2])
            elif operasi[1] == '/' :
                result = int(operasi[0]) / int(operasi[2])
            string_balasan = ', ' + data + ', ' + str(result)
            total_res += result

            for client_address in client_list :
                string_list.append(client_address[0] + ', ' + str(client_address[1]) + string_balasan)

            print(string_list)

            for client_socket in client_socket_list :
                print client_socket
                # try:
                client_socket.send('\n'.join(string_list[-2:]))
                # except:
                #     pass
            
            print client_list
        

        # close socket client
        # client_socket.close()

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)