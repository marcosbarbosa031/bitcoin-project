import ecdsa

class PublicKey(object):
    def __init__(self, private_key):
        self.private_key = private_key
    
    def generate_key(self):
        # This is your private signature.
        self.signed_key = ecdsa.SigningKey.from_string(self.private_key.decode("hex"), curve = ecdsa.SECP256k1)

        # This is a public verification key.
        verification_key = self.signed_key.verifying_key

        # Generating your public key based on your verification key.
        return ('\04' + verification_key.to_string()).encode("hex")

    def sign_msg(self, hashed_rtx)  :
        return self.signed_key.sign_digest(hashed_rtx, sigencode = ecdsa.util.sigencode_der)
    pass
