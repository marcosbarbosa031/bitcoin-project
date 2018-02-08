import struct
import hashlib

class ConnHeader(object):

    def __init__(self):
        self.magic = "F9BEB4D9".decode("hex")

        # "\00" = NULL
        self.command = "version" + 5 * "\00"
    
    def create_header(self, payload):
        length = struct.pack("L", len(payload))
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

        return self.magic + self.command + length + checksum + payload
    pass
