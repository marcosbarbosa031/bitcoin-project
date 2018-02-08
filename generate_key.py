import hashlib
import base58
from key.private_key import PrivateKey
from key.public_key import PublicKey


# Network Codes
MAIN_NETWORK = '\00'
TEST_NETWORK = '\6f'
NAMECOIN_NETWORK = '\34'

############################### Creating the Public and Private keys ####################################

# Generating your private key.
priv_k = PrivateKey()
priv_k.set_random_key()
private_key = priv_k.private_key

# Generating your public key from the private key.
pub_k = PublicKey(private_key)
public_key = pub_k.generate_key()

#########################################################################################################

################################## Creating the Bitcoin Address #########################################

# Create an instance of the ripemd160 class
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
