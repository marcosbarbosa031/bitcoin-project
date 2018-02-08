import struct
import time
import random
import hashlib
import socket

version = struct.pack("I", 70015)

# Service = 8 bytes unsigned integer.
# 0 = not-full node.
services = struct.pack("Q", 0)

# Timestamp = 8 bytes unsigned integer.
timestamp = struct.pack("Q", time.time())

# Recieving Service = 8 bytes unsigned integer.
addr_recv_services = struct.pack("Q", 0) # services.

# Recieving IP = 16 bytes char Big Endian.
addr_recv_ip = struct.pack(">16s", "127.0.0.1")

# Transmiting Port = 2 bytes unsigned integer Big Endian.
# 8333 = Default port bitcoin protocol.
addr_recv_port = struct.pack(">H", 8333)

addr_trans_services = struct.pack("Q", 0)  # services.

# Transmiting IP = 16 bytes char Big Endian.
addr_trans_ip = struct.pack(">16s", "127.0.0.1")

# Transmiting Port = 2 bytes unsigned integer Big Endian.
# 8333 = Default port bitcoin protocol.
addr_trans_port = struct.pack(">H", 8333)

nonce = struct.pack("Q", random.getrandbits(64))

user_agent_bytes = struct.pack("B", 0)

start_height = struct.pack("L", 508198)

# Relay = boolean.
# True = Can recieve incoming transactions.
# False = Ignore incoming transactions
relay = struct.pack("?", False)

payload = version + services + timestamp + addr_recv_services + addr_recv_ip + addr_recv_port + addr_trans_services + addr_trans_ip + addr_trans_port + nonce + user_agent_bytes + start_height + relay

# Header of the message

magic = "F9BEB4D9".decode("hex")
# "\00" = NULL
command = "version" + 5 * "\00"

length = struct.pack("L", len(payload))

checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

message = magic + command + length + checksum + payload

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "66.90.137.89"
PORT = 8333

s.connect((HOST, PORT))

s.send(message)

s.recv(1024)