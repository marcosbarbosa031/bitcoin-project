import struct
import hashlib

class ConnHeader(object):

    def __init__(self):
        self.magic = "F9BEB4D9".decode("hex")

        # "\00" = NULL
        self.command = "tx" + 10 * "\00"
    
    def create_header(self, payload):
        self.length = struct.pack("L", len(payload))
        self.checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

        return self.magic + self.command + self.length + self.checksum + payload
    pass
