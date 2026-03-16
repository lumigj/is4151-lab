import socket
import _thread as thread



def service_client(client_socket, address):
	
	print("Connection from: " + str(address))
	
	while True:

		data = client_socket.recv(1024).decode('utf-8')
		
		if not data:

			break
		
		print('From online user {} -> {}'.format(address, data))
		data = data.upper()
		client_socket.send(data.encode('utf-8'))
	
	client_socket.close()



def server():
	
	try:
		
		host = socket.gethostname()
		port = 8888

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((host, port))		
		
		while True:		
			
			s.listen(1)			
			client_socket, address = s.accept()
			# s.setblocking(False)
			thread.start_new_thread(service_client, (client_socket, address))
	
	except KeyboardInterrupt:
		
		print('Program terminated!')
	
	except Exception as e:
		
		print('An unknown error occurred: ' + str(e))
	
	finally:
		
		s.close()



if __name__ == '__main__':
	server()