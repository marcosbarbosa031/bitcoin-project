import os
import ecdsa
import hashlib
import base58

MAIN_NETWORK = '\00'
TEST_NETWORK = '\6f'
NAMECOIN_NETWORK = '\34'

############################### Creating the Public and Private keys ####################################

# Generating your private key
private_key = os.urandom(32).encode("hex")

# This is your private signature
signed_key = ecdsa.SigningKey.from_string(private_key.decode("hex"), curve = ecdsa.SECP256k1)

# This is a public verification key
verification_key = signed_key.verifying_key

# Generating your publickey based on on your verification key
public_key = ('\04' + verification_key.to_string()).encode("hex")

#########################################################################################################

################################## Creating the Bitcoin Address #########################################

ripemd160 = hashlib.new('ripemd160')

ripemd160.update(hashlib.sha256(public_key.decode("hex")).digest())

middle_man = MAIN_NETWORK + ripemd160.digest()

checksum = hashlib.sha256(hashlib.sha256(middle_man).digest()).digest()[:4]

bitcoin_addr = base58.b58encode(middle_man + checksum)

#########################################################################################################

print "This is your Private Key: " + private_key
print "This is your Public Key: " + public_key
print "This is your Bitcoin Address: " + bitcoin_addr
