import struct

prev_txid = "0db085dcc0ec7d057f6456ae97519b67eae4b937074ea6d8befdd5ee4f7a6b9c"

class transactionIn(object):
    
    def __init__(self, txouthash):
        self.txouthash      = txouthash
    pass


class rawTransaction(object):
    version     = struct.pack("<L", 1)
    lock_time   = struct.pack("<L", 0)

    def __init__(self, tx_in_count, tx_out_count, tx_in):
        self.tx_in_count     = struct.pack("<L", tx_in_count)
        self.tx_in       = {
            'txouthash'     : tx_in.txouthash,
            'tx_in_index'   : struct.pack("<L", 0)
        }
        self.tx_out_count    = struct.pack("<B", tx_out_count)
        self.tx_out          = {} #TEMP

    pass


def flip_byte_order(string):
    flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
    return flipped


txin = transactionIn(flip_byte_order(prev_txid).decode("hex"))

rtx = rawTransaction(1, 2, txin)

print rtx.tx_in
