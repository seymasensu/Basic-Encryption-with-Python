#import the socket
import socket as sk

from sys import argv

from ssl import *

import hashlib  #import the hash library

# creating the socket
server_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

#allow to reuse the address

server_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)


#if there are two arguments,first one is the name of the script and the second one is the port number, if the number of arguments are diffrent from 2, ask for the port number
if len(argv) ==2: 
	port = int(argv[1]) # convert argument into integer
else:
	port = int(input("Enter port number: "));
	
while True:
	try:
		#try to bind the socket to the port
		server_socket.bind(('', port))
		break
	except ConnectionRefusedError:#if the port number or name is wrong
		print("Unable to connect")
		
	
	except sk.error:#if there is any other errror
		print("Invalid port number.")
		choise = input("Retry, Change port, Quit: ")
		
		#[0] means first character of the word, 
		if choise.lower()[0] == "c": # c means change details
			#convert it to lowercase
			
			
			#input a new port number for the server
			port= int(input("Enter the port number of the server: "))
		elif choise.lower()[0] == "q": # quit the program
			exit() # terminate the program


#Starting the socket listening
server_socket.listen(1) # Only 1 client is allowed to queue

#wrapping the socket of the server
tls_server = wrap_socket(server_socket, ssl_version=PROTOCOL_TLSv1, cert_reqs=CERT_NONE, server_side=True, keyfile='./keyfile.pem', certfile='./certfile.pem')

#Print statement for connection is successful
print("Server is listening on port : ",port)

#waiting for the client to connect
connection, client_address = tls_server.accept()
print("Connection connection from: ", client_address)

#function for coverting the data into a encrypted code and the parameterr of this function is the message entered by the user
def hashing(my_string):
	hash_sha = hashlib.sha256(my_string.encode()).hexdigest()      #First encode the message, and then convert it into a encrypted code
	return hash_sha                         #return the encrypted message
	
# using a while loop to keep going
while True:
	
	#receivng the data from the client and settig the byte size to 1024
	data_in = connection.recv(1024)

	
	#decoding the data as binary instead of text
	message = data_in.decode()
			
			
	#printing the data sent from the client
	print("received from client: ", message)
	
	#If user enters q breaks out of the loop
	if message.strip()=='q':
		break
				

	#sending the data back
	sha_signature = hashing(message)      #send the message to the hashing function
	connection.send(sha_signature.encode() )


# First, shutting down the connection and then, closing the connection
		
connection.shutdown(sk.SHUT_RDWR)
connection.close()
# First, shutting down the socket and then, closing the socket
tls_server.shutdown(sk.SHUT_RDWR)
tls_server.close()



