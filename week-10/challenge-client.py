import pickle
import socket
import sys
import select
import os

server_address = ('127.0.0.1',5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

game_state = ['_'] * 10

input_socket = [client_socket, sys.stdin]

player = sys.argv[1]

def game_board(state):
    global game_state
    for item in '123456789':
        game_state[int(item)] = state[int(item)]
    
    print '{0}|{1}|{2}'.format(game_state[1],game_state[2],game_state[3])
    print '{0}|{1}|{2}'.format(game_state[4],game_state[5],game_state[6])
    print '{0}|{1}|{2}'.format(game_state[7],game_state[8],game_state[9])

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        for sock in read_ready:
            if sock == client_socket :
                state = client_socket.recv(1024)
                if state == 'WAIT':
                    print 'waiting'
                else :
                    if state == 'OK':
                        game_board(game_state)
                    elif state == 'WIN':
                        print 'You Win'
                        client_socket.close()
                        sys.exit()
                    elif state == 'LOSE':
                        print 'You Lose'
                        client_socket.close()
                        sys.exit()
                    else :
                        state = pickle.loads(state)
                        game_board(state)
                    print 'select [1-9] :'
            else :
                message = sys.stdin.readline()
                message = message.strip()
                os.system("clear")
                game_state[int(message)] = player
                state = pickle.dumps(game_state)
                client_socket.send(state)       
        

except KeyboardInterrupt:
    client_socket.close()
    sys.exit()
