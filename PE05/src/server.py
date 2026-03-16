import socket



def server():
	
	try:
	
		host = socket.gethostname()
		port = 8888

		s = socket.socket()
		s.bind((host, port))

		s.listen(1)
		client_socket, adress = s.accept()
		
		print("Connection from: " + str(adress))
		
		while True:
			data = client_socket.recv(1024).decode('utf-8')
			
			if not data:
				break
			
			print('From online user: ' + data)
			data = data.upper()
			client_socket.send(data.encode('utf-8'))
		
		client_socket.close()
	
	except KeyboardInterrupt:		
		
		print('Program terminated!')
	
	except Exception as e:
		
		print('An unknown error occurred: ' + str(e))
	
	finally:
		
		s.close()



if __name__ == '__main__':
	
	server()