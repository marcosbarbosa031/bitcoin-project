import struct
import time
import random

class ConnMessage(object):
    
    def __init__(self, version, service, addr_recv_services, addr_recv_ip, addr_recv_port, addr_trans_services, addr_trans_ip, addr_trans_port, user_agent_bytes, start_height, relay):
        # Version = 4 bytes unsigned integer.
        self.version = struct.pack("I", version)

        # Service = 8 bytes unsigned integer.
        # 0 = not-full node.
        self.services = struct.pack("Q", service)

        # Timestamp = 8 bytes unsigned integer.
        self.timestamp = struct.pack("Q", time.time())

        # Recieving Service = 8 bytes unsigned integer.
        self.addr_recv_services = struct.pack("Q", addr_recv_services)

        # Recieving IP = 16 bytes char Big Endian.
        self.addr_recv_ip = struct.pack(">16s", addr_recv_ip)

        # Transmiting Port = 2 bytes unsigned integer Big Endian.
        # 8333 = Default port bitcoin protocol.
        self.addr_recv_port = struct.pack(">H", addr_recv_port)

        # Transmiting Service = 8 bytes unsigned integer.
        self.addr_trans_services = struct.pack("Q", addr_trans_services)

        # Transmiting IP = 16 bytes char Big Endian.
        self.addr_trans_ip = struct.pack(">16s", addr_trans_ip)

        # Transmiting Port = 2 bytes unsigned integer Big Endian.
        # 8333 = Default port bitcoin protocol.
        self.addr_trans_port = struct.pack(">H", addr_trans_port)

        # Nonce = 8 bytes unsigned integer.
        self.nonce = struct.pack("Q", random.getrandbits(64))

        #User Agent = 1 byte unsigned character.
        self.user_agent_bytes = struct.pack("B", user_agent_bytes)

        # Start Height = 4 bytes unsigned integer.
        self.start_height = struct.pack("I", start_height)

        # Relay = boolean.
        # True = Can recieve incoming transactions.
        # False = Ignore incoming transactions
        self.relay = struct.pack("?", relay)
     
    def create_message(self):

        return self.version + self.services + self.timestamp + self.addr_recv_services + self.addr_recv_ip + self.addr_recv_port + self.addr_trans_services + self.addr_trans_ip + self.addr_trans_port + self.nonce + self.user_agent_bytes + self.start_height + self.relay

    pass
