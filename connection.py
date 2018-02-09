import socket
from conn.conn_header import ConnHeader
from conn.conn_message import ConnMessage

###################################### Creating the message ######################################

# For more details: See conn_message.py 
msg = ConnMessage(70015, 0, 0, "127.0.0.1", 8333, 0, "127.0.0.1", 8333, 0, 508198, False)
payload = msg.create_message()

##################################################################################################

###################################### Header of the message #####################################

# For more details: See conn_header.py
header = ConnHeader()
message = header.create_header(payload)

##################################################################################################

#################################### Preparing the connection ####################################

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "66.90.137.89"
PORT = 8333

s.connect((HOST, PORT))

s.send(message)

s.recv(1024)

##################################################################################################
