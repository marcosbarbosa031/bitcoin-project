import struct
import base58
import hashlib
from key.public_key import PublicKey
from connection import Connection

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
        self.tx_in          = tx_in
        self.tx_out_count   = struct.pack("<B", tx_out_count)
        self.tx_out1        = tx_out1
        self.tx_out2        = tx_out2
    
    def make_transaction(self, sender_private_key):
        rtx_string = (
            self.version + 
            self.tx_in_count + 
            self.tx_in.txouthash + 
            self.tx_in.tx_out_index + 
            self.tx_in.tx_in_script_bytes + 
            self.tx_in.tx_in_script + 
            self.tx_in.tx_in_sequence + 
            self.tx_out_count + 
            self.tx_out1.tx_out_value + 
            self.tx_out1.tx_out_pk_script_bytes + 
            self.tx_out1.tx_out_pk_script + 
            self.tx_out2.tx_out_value +
            self.tx_out2.tx_out_pk_script_bytes +
            self.tx_out2.tx_out_pk_script + 
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
            self.tx_in.txouthash +
            self.tx_in.tx_out_index +
            struct.pack("<B", len(sigscript) + 1) +
            struct.pack("<B", len(signature) + 1) +
            sigscript + 
            self.tx_in.tx_in_sequence +
            self.tx_out_count +
            self.tx_out1.tx_out_value +
            self.tx_out1.tx_out_pk_script_bytes +
            self.tx_out1.tx_out_pk_script +
            self.tx_out2.tx_out_value +
            self.tx_out2.tx_out_pk_script_bytes +
            self.tx_out2.tx_out_pk_script +
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

# rtx_message = rtx.make_transaction(sender_private_key).encode("hex")
rtx_message = "01000000015cd81501e2a63c942fcb24de76d4532406156c8cb10b5dcb123a1cb5be13d884000000008a473044022050ac959cd6b584c7340e764491925da8570599936843b75053f964fea0c26b7302203b49d64de9d2625c48ceea72178e158d44d0273d7b7774e31145358a32d8400501410437078f8c4a54b67cd1724a3535cb1918bca186c7a143459c9aac35113d4a958b0d4eea6b320fa82c17147b72e0fe11c08b0054897ffb7bdb194f259b0db9e129ffffffff02a0860100000000001976a914478075922af41fb441aa0ab67e91aef27ef1e68688ac50c30000000000001976a914ec06b2bf18c89706855f761d215f21f3315b399488ac00000000"

# Preparing connection

conn = Connection()
conn.createMessage(rtx_message)
conn.sendMessage()

# print (rtx.make_transaction(sender_private_key).encode("hex"))
# print rtx.tx_in.tx_in_script_bytes.encode("hex")


# 01000000                                                          - Version
# 01                                                                - No.Inputs
# 5cd81501e2a63c942fcb24de76d4532406156c8cb10b5dcb123a1cb5be13d884  - OUT ID
# 00000000                                                          - OUT indez number
# 8c49                                                              - sigscript size
# 3046022100954eb564a3f0e45dc2203681a5d058d3378933b7586a5a9d95dfeb
# a73949e306022100a9ecc813ae95f27020962b6b230f6221d6dd7c97cd840685
# cdf05763fdf9ee1501410437078f8c4a54b67cd1724a3535cb1918bca186c7a1
# 43459c9aac35113d4a958b0d4eea6b320fa82c17147b72e0fe11c08b0054897f
# fb7bdb194f259b0db9e129                                            - Sigscript
# ffffffff                                                          - Sequence
# 02                                                                - No.Outputs
# ------------------------ Output 1 ------------------------------
# a086010000000000                                                  - Satoshi
# 19                                                                - Bytes in publickey
# 76                                                                - OP_DUP
# a9                                                                - OP_HASH160
# 14                                                                - Push 20 bytes as data
# 478075922af41fb441aa0ab67e91aef27ef1e686                          - Publickey Hash
# 88                                                                - OP_EQUALVERIFY
# ac                                                                - OP_CHECKSIG
# ------------------------ Output 2 ------------------------------
# 50c3000000000000                                                  - Satoshi                        
# 19                                                                - Bytes in publickey
# 76                                                                - OP_DUP
# a9                                                                - OP_HASH160
# 14                                                                - Push 20 bytes as data
# ec06b2bf18c89706855f761d215f21f3315b3994                          - Publickey Hash
# 88                                                                - OP_EQUALVERIFY
# ac                                                                - OP_CHECKSIG
# 00000000                                                          - locktime


# 01000000
# 01
# 5cd81501e2a63c942fcb24de76d4532406156c8cb10b5dcb123a1cb5be13d884
# 00000000
# 8b48
# 3045022012ae609c5a7f11cc3d061e9f996ab54de856eefd945965d4fd26d6ad6fa9ea59022100b080fbd3e3b27d9604d8743367e5ce996063b00c6676145f7c03a6d5ab89af2c01410437078f8c4a54b67cd1724a3535cb1918bca186c7a143459c9aac35113d4a958b0d4eea6b320fa82c17147b72e0fe11c08b0054897ffb7bdb194f259b0db9e129ffffffff02a0860100000000001976a914478075922af41fb441aa0ab67e91aef27ef1e68688ac50c30000000000001976a914ec06b2bf18c89706855f761d215f21f3315b399488ac00000000
