import struct
import base58
import hashlib
from key.public_key import PublicKey

prev_txid           = "84d813beb51c3a12cb5d0bb18c6c15062453d476de24cb2f943ca6e20115d85c"

sender_address      = "1NWzVg38ggPoVGAG2VWt6ktdWMaV6S1pJK"
sender_hashed_pk    = base58.b58decode_check(sender_address)[1:].encode("hex")
sender_private_key  = "CF933A6C602069F1CBC85990DF087714D7E86DF0D0E48398B7D8953E1F03534A"

receiver_address    = "17X4s8JdSdLxFyraNUDBzgmnSNeZpjm42g"
receiver_hashed_pk  = base58.b58decode_check(receiver_address)[1:].encode("hex")

class transactionIn(object):
    
    def __init__(self, txouthash, tx_out_index, sender_hashed_pk):
        self.txouthash          = txouthash
        self.tx_out_index       = struct.pack("<L", tx_out_index)
        self.tx_in_script       = ("76a914%s88ac" % sender_hashed_pk).decode("hex")
        self.tx_in_script_bytes = struct.pack("<B", len(self.tx_in_script)) 
        self.tx_in_sequence     = "ffffffff".decode("hex")
    pass


class transactionOut(object):

    def __init__(self, BTC, receiver_hashed_pk):
        self.tx_out_value           = struct.pack("<Q", (BTC * 100000000)) # Convert to Satoshi
        self.tx_out_pk_script       = ("76a914%s88ac" % receiver_hashed_pk).decode("hex")
        self.tx_out_pk_script_bytes = struct.pack("<B", len(self.tx_out_pk_script))
    pass


class rawTransaction(object):
    version     = struct.pack("<L", 1)
    lock_time   = struct.pack("<L", 0)

    def __init__(self, tx_in_count, tx_out_count, tx_in, tx_out1, tx_out2):
        self.tx_in_count    = struct.pack("<B", tx_in_count)
        self.tx_in          = {
            'txouthash'             : tx_in.txouthash,
            'tx_out_index'          : tx_in.tx_out_index,
            'tx_in_script'          : tx_in.tx_in_script,
            'tx_in_script_bytes'    : tx_in.tx_in_script_bytes,
            'tx_in_sequence'        : tx_in.tx_in_sequence
        }
        self.tx_out_count   = struct.pack("<B", tx_out_count)
        self.tx_out1        = {
            'tx_out_value'          : tx_out1.tx_out_value,
            'tx_out_pk_script'      : tx_out1.tx_out_pk_script,
            'tx_out_pk_script_bytes': tx_out1.tx_out_pk_script_bytes
        } #TEMP
        self.tx_out2        = {
            'tx_out_value'          : tx_out2.tx_out_value,
            'tx_out_pk_script'      : tx_out2.tx_out_pk_script,
            'tx_out_pk_script_bytes': tx_out2.tx_out_pk_script_bytes
        } #TEMP
    
    def make_transaction(self, sender_private_key):
        rtx_string = (
            self.version + 
            self.tx_in_count + 
            self.tx_in['txouthash'] + 
            self.tx_in['tx_out_index'] + 
            self.tx_in['tx_in_script_bytes'] + 
            self.tx_in['tx_in_script'] + 
            self.tx_in['tx_in_sequence'] + 
            self.tx_out_count + 
            self.tx_out1['tx_out_value'] + 
            self.tx_out1['tx_out_pk_script_bytes'] + 
            self.tx_out1['tx_out_pk_script'] + 
            self.tx_out2['tx_out_value'] +
            self.tx_out2['tx_out_pk_script_bytes'] +
            self.tx_out2['tx_out_pk_script'] + 
            self.lock_time + 
            struct.pack("<L", 1)
        )
        hashed_rtx = hashlib.sha256(hashlib.sha256(rtx_string).digest()).digest()
        pubk = PublicKey(sender_private_key)

        public_key = pubk.generate_key()
        signature = pubk.sign_msg(hashed_rtx)
        
        sigscript = (
            signature + 
            '\01' + 
            struct.pack("<B", len(public_key.decode("hex"))) +
            public_key.decode("hex")
        )

        real_tx = (
            self.version +
            self.tx_in_count +
            self.tx_in['txouthash'] +
            self.tx_in['tx_out_index'] +
            struct.pack("<B", len(sigscript) + 1) +
            struct.pack("<B", len(signature) + 1) +
            sigscript + 
            self.tx_in['tx_in_sequence'] +
            self.tx_out_count +
            self.tx_out1['tx_out_value'] +
            self.tx_out1['tx_out_pk_script_bytes'] +
            self.tx_out1['tx_out_pk_script'] +
            self.tx_out2['tx_out_value'] +
            self.tx_out2['tx_out_pk_script_bytes'] +
            self.tx_out2['tx_out_pk_script'] +
            self.lock_time
        )
        return real_tx
    pass


def flip_byte_order(string):
    flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
    return flipped


txin    = transactionIn(flip_byte_order( prev_txid).decode("hex"), 0, sender_hashed_pk)
txout1  = transactionOut(0.001, receiver_hashed_pk)
txout2  = transactionOut(0.0005, sender_hashed_pk)

rtx = rawTransaction(1, 2, txin, txout1, txout2)

# print rtx.tx_in['tx_in_script'].encode("hex")
print rtx.make_transaction(sender_private_key).encode("hex")
