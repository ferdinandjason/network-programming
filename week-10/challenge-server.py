import socket
import select
import sys
import time
import pickle

server_address = ('127.0.0.1',5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
client_socket_list = []

first = True

def check_win(s):
    if(s[1] == s[2] and s[2] == s[3] and s[3] != '_') : return True
    if(s[4] == s[5] and s[5] == s[6] and s[6] != '_') : return True
    if(s[7] == s[8] and s[8] == s[9] and s[9] != '_') : return True
    if(s[1] == s[4] and s[4] == s[7] and s[7] != '_') : return True
    if(s[2] == s[5] and s[5] == s[8] and s[8] != '_') : return True
    if(s[3] == s[6] and s[6] == s[9] and s[9] != '_') : return True
    if(s[1] == s[5] and s[5] == s[9] and s[9] != '_') : return True
    if(s[3] == s[5] and s[5] == s[7] and s[7] != '_') : return True

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket :
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                client_socket_list.append(client_socket)
                if first == True :
                    first = False
                    client_socket.send('OK')
                    time.sleep(0.1)
                else :
                    client_socket.send('WAIT')
                    time.sleep(0.1)
            else:
                data = sock.recv(1024)
                try :
                    game_state = pickle.loads(data)
                    win = check_win(game_state)
                    for client in client_socket_list:
                        if client == sock :
                            client.send('WAIT')
                            time.sleep(0.1)
                            if win :
                                client.send('WIN')
                                time.sleep(0.1)
                        else :
                            if win :
                                client.send('LOSE')
                                time.sleep(0.1)
                            else :
                                state = pickle.dumps(game_state)
                                client.send(state)
                                time.sleep(0.1)
                except:
                    server_socket.close()
                    sys.exit(0)                
            
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)