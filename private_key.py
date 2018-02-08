import os

class PrivateKey(object):

    def generate_key(self):
        # Random 32 bytes Hexadecimal key.
        return os.urandom(32).encode("hex")
    pass
