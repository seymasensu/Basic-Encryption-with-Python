#import the socket
import socket as sk

from sys import argv

from ssl import *

from easygui import *

# creating the socket
client_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

#Do we have the server address from command-line arguments

#if there are three arguments, the first one is the name of the script, second one is the ip address and the third one is the port number, if the number of arguments are diffrent from 3, ask for the info (host number and port number)
if len(argv) ==1:
	host = enterbox("Enter server's hostname or ip address: ")
	port= int(enterbox("Enter the port number of the server: "))
elif len(argv) ==2:
	host = argv[1]
	port= int(enterbox("Enter the port number of the server: "))
elif len(argv) ==3:
	
	host = argv[1]
	port = int(argv[2]) # convert argument into integer
	print("Server: ",host," on port ",port)
else:
	msgbox("Incorrect number of command line arguments")
	exit() # terminating the program

#wrapping the socket with tls
tls_client = wrap_socket(client_socket, ssl_version=PROTOCOL_TLSv1, cert_reqs=CERT_NONE)

while True:
	try:
		#try to connect to the server using the specified address (host,port)
		tls_client.connect((host, port))
		break
	except ConnectionRefusedError:#if the port number or name is wrong
		msgbox("Unable to connect")
		
	except sk.gaierror: 
		msgbox("Invalid hostname")
		
	except IOError:
		msgbox("Input Output error")
	except ValueError:
		msgbox("Inappropriate value type")
	except KeyboardInterrupt:
		msgbox('Program terminated')
		
	options=["quit", "change server details", "retry"]
	chosen_option=buttonbox(msg="",title="connection error", choices= options)

		
	if chosen_option == "change server details" : #change server details and try again
		host= enterbox("Enter server's hostname or IP address: ")
		port= int(enterbox("Enter the port number of the server: "))
	elif chosen_option == "quit" : # quit the program
		exit() #terminate the program
#creating a dictionary	
words={}  

# using a while loop to keep going
while True:
	
	# asking user to enter a message they wish to send
	message=enterbox("Enter a message to send or enter q to quit: ")
	
	# encoding the user's data as a bytes sequence
	data_out = message.encode()

	# sends the data after encoding it
	tls_client.send(data_out)
		
	#If user enters q breaks out of the loop
	if message.strip() == 'q':
		break
		
	#receivng the data and settig the byte size to max 1024
	data_in = tls_client.recv(1024)
	
	# decoding the received hashed message to display it
	hashed_message = data_in.decode()
	
	
	words[message]=hashed_message # assignin the hashed message's words to the dictionary named words
	print('Received messages from the server: ' )
	for keys,values in words.items():    #for loop for printing both original message and hashed message
		print(keys + " --> " + values)
		


# First, shutting down the socket
tls_client.shutdown(sk.SHUT_RDWR)

# And then, closing the socket
tls_client.close()


