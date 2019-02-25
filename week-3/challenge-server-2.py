import socket
import select
import Queue
from threading import Thread
from time import sleep
from random import randint
import sys
 
class ProcessThread(Thread):
	def __init__(self):
		super(ProcessThread, self).__init__()
		self.running = True
		self.q = Queue.Queue()
 
	
	def add(self, data):
		self.q.put(data)
		print(data)
 
	def stop(self):
		self.running = False

	def run(self):
		q = self.q
		while self.running:
			try:
				# block for 1 second only:
				value = q.get(block=True, timeout=1)
				process(value)
			except Queue.Empty:
				sys.stdout.write('.')
				sys.stdout.flush()
		#
		if not q.empty():
			print "Elements left in the queue:"
			while not q.empty():
				print q.get()

t = ProcessThread()
t.start()

def process(value):
	"""
	Implement this. Do something useful with the received data.
	"""
	print value
	sleep(randint(1,5))	# emulating processing time

def main():
	s = socket.socket()				# Create a socket object
	host = 'localhost' # Get local machine name
	port = 5020					  # Reserve a port for your service.
	s.bind((host, port))				 # Bind to the port
	print "Listening on port {p}...".format(p=port)
 
	s.listen(5)				 # Now wait for client connection.
	readylist = [s,]
	while True:
		try:
			ready, a, b = select.select(readylist,[], [])
			for c in ready:
				if c == s:
					client, addr = s.accept()
					readylist.append(client)
				else :
					data = client.recv(4096)
					#print data
					t.add(data[:-1])
		except KeyboardInterrupt:
			print
			print "Stop."
			cleanup()
			break
		except socket.error, msg:
			print "Socket error! %s" % msg
			cleanup()
			break

def cleanup():
	t.stop()
	t.join()
 
 
if __name__ == "__main__":
	main()


		
