import socket
import threading
import sys

MAX_BUFFER = 1024

class Client:
	def __init__(self, address, port, reply_port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.address = address
		self.port = port
		self.reply_port = reply_port

	def create_reply_connection(self):
		reply_address = (self.address, self.reply_port)

		self.reply_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.reply_socket.bind(reply_address)
		self.reply_socket.listen(5)

	def reply_listener(self):
		try:
			server_reply_socket , _ = self.reply_socket.accept()
		except:
			pass

		reply = server_reply_socket.recv(MAX_BUFFER)
		if reply[-3:] == 'END':
			self.socket.close()
			sys.exit()
		print reply

		self.reply_socket.close()

	def create_connection(self):
		server_address = (self.address, self.port)
		self.socket.connect(server_address)

	def start(self):
		self.create_connection()
		self.create_reply_connection()

		while True:
			try:
				command = raw_input('math> ')
				self.socket.send(command)
				reply_thread = threading.Thread(target=self.reply_listener)
				reply_thread.start()
			except KeyboardInterrupt:
				self.socket.close()
				sys.exit(0)

client = Client('localhost',5000, 5001)
client.start()