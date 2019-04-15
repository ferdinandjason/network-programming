import socket
import select
import sys
import os

server_address = ('127.0.0.1',80)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)

            else :
                # receive data from client, break when null received
                data = sock.recv(4096)
                print data
                
                request_header = data.split('\r\n')
                print(request_header)
                request_file = request_header[0].split()[1]

                path = '.'+request_file

                if os.path.isdir(path) :
                    dirs = os.listdir(path)
                    response_data = """
    <!DOCTYPE html>
    <html>

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Coba Proghar</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body>
                    """
                    try:
                        asd = path.split('/')[2]
                        asd = path.split('/')[1:]
                        print('asdasd"'+asd)
                        asd = '/'.join(asd)
                        
                    except:
                        pass

                    if path != './' : 
                        response_data += "<a href='/'>"+".."+"</a><br/>"

                    for dir in dirs:
                        response_data += "<a href='"+dir+"'>"+dir+"</a><br/>"

                    response_data += "</body></html>"

                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:'+ str(content_length)+'\r\n\r\n'
                    print(response_data)

                    sock.send(response_header + response_data)

                else :
                    path = path[2:]
                    try :
                        f = open(path, 'r')
                        response_data = f.read()
                        f.close()
                    except:
                        pass
                    response_header = 'HTTP/1.1 200 OK\r\n'+"Content-Disposition: attachment; filename="+path+"\r\n"+"Content-Type: application/force-download\r\n"+"Content-Transfer-Encoding: binary\r\n"+"Content-Length: "+str(len(response_data))+'\r\n\r\n'

                    sock.send(response_header + response_data)

except KeyboardInterrupt:
    server_socket.close()
    os.system('python2 challenge-server.py')
    sys.exit(0)
    