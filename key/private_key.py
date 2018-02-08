import os

class PrivateKey(object):

    def set_random_key(self):
        # Random 32 bytes Hexadecimal key.
        self.private_key = os.urandom(32).encode("hex")

    def set_key(self, private_key):
        self.private_key = private_key
    pass
