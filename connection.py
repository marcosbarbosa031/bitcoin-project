import socket
from conn.conn_header import ConnHeader

class Connection(object):
    def __init__(self):
        self.HOST = "66.90.137.89"
        self.PORT = 8333
    
    def setHost(self, host):
        self.HOST = host
    
    def getHost(self):
        return self.HOST
    
    def setPort(self, port):
        self.PORT = port

    def getPort(self):
        return self.PORT

    def createMessage(self, message):
        header = ConnHeader()
        self.message = header.create_header(message)
    
    def sendMessage(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        s.send(self.message)
        s.recv(1024)
    
    pass

###################################### Creating the message ######################################

# For more details: See conn_message.py
# msg = ConnMessage(70015, 0, 0, "127.0.0.1", 8333, 0, "127.0.0.1", 8333, 0, 508198, False)
# payload = msg.create_message()

##################################################################################################

###################################### Header of the message #####################################

# For more details: See conn_header.py
# header = ConnHeader()
# message = header.create_header(payload)

##################################################################################################

#################################### Preparing the connection ####################################

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# HOST = "66.90.137.89"
# PORT = 8333

# s.connect((HOST, PORT))

# s.send(message)

# s.recv(1024)

##################################################################################################
