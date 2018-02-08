import os
import ecdsa
import hashlib
import base58


# Network Codes
MAIN_NETWORK = '\00'
TEST_NETWORK = '\6f'
NAMECOIN_NETWORK = '\34'

############################### Creating the Public and Private keys ####################################

# Generating your private key.
private_key = os.urandom(32).encode("hex")

# This is your private signature.
signed_key = ecdsa.SigningKey.from_string(private_key.decode("hex"), curve = ecdsa.SECP256k1)

# This is a public verification key.
verification_key = signed_key.verifying_key

# Generating your public key based on your verification key.
public_key = ('\04' + verification_key.to_string()).encode("hex")

#########################################################################################################

################################## Creating the Bitcoin Address #########################################

ripemd160 = hashlib.new('ripemd160')

# Do a ripemd160 hash of a SHA256 hash of your public key.
ripemd160.update(hashlib.sha256(public_key.decode("hex")).digest())

# Add the Network code in the begining of you ripemd160 hash.
middle_man = MAIN_NETWORK + ripemd160.digest()

# Make the checksum by double SHA256 hashing the previous data.
checksum = hashlib.sha256(hashlib.sha256(middle_man).digest()).digest()[:4]

# Convert base256 to base58 the data plus it checksum to geneate your bitcoin address.
bitcoin_addr = base58.b58encode(middle_man + checksum)

#########################################################################################################

print "This is your Private Key: " + private_key
print "This is your Public Key: " + public_key
print "This is your Bitcoin Address: " + bitcoin_addr
