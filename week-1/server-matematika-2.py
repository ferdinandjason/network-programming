import socket
import threading
import sys

MAX_BUFFER = 1024


class ServerThread(threading.Thread):
    def __init__(self, (client, client_address), server, reply_port):
        threading.Thread.__init__(self)

        self.client = client
        self.client_address = client_address
        self.server = server

    def parse_data(self, data):
        math = data.split(' ')
        math[0] = int(math[0])
        math[2] = int(math[2])

        result = math[0]

        if math[1] == '+':
            result += math[2]
        elif math[1] == '-':
            result -= math[2]
        elif math[1] == '*':
            result *= math[2]
        elif math[1] == '/':
            result /= math[2]


        return result

    def run(self):
		print 'client connected: ' + str(self.client_address) + '\n'
		try:
			while True:
				data = self.client.recv(MAX_BUFFER)
				print data
				if data == 'END':
					self.server.broadcast(
					    'TOTAL AKHIR : ' + str(self.server.total_result) + ' END')
					self.client.close()
				else:
					result = self.parse_data(data)

					self.server.total_result += result
					reply_message = data + ',' + str(result)
					self.server.broadcast(reply_message)
		except Exception:
			pass


class Server:
    def __init__(self, port, reply_port):
        self.address = 'localhost'

        self.port = port
        self.reply_port = reply_port

        self.total_result = 0
        self.clients = []

    def start_server_socket(self):
        server_address = (self.address, self.port)

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(server_address)
        self.server_sock.listen(5)

    def start_reply_socket(self):
        reply_address = (self.address, self.reply_port)

        self.reply_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reply_sock.connect(reply_address)

    def start(self):
        self.start_server_socket()
        try:
            while True:
                thread = ServerThread(self.server_sock.accept(), self, self.reply_port)
                thread.daemon = True
                thread.start()

                self.clients.append(thread)

        except KeyboardInterrupt:
            print 'Closing socket connection'
            self.server_sock.close()
            sys.exit(0)

    def broadcast(self, message):
        self.start_reply_socket()
        for client in self.clients:
            header = str(client.client_address[0]) + \
                ',' + str(client.client_address[1]) + ','
            self.reply_sock.send(header+message)
	self.reply_sock.close()


server = Server(5000, 5001)
server.start()
