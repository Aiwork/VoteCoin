import rlp

GENESIS_PREVHASH=b'\x00' * 32

class Block(rlp.Serializable):
    FIELDS = ['prevhash', 'timestamp', 'number']

    def __init__(self,
                 nonce,
                 number,
                 prevhash=GENESIS_PREVHASH):
        fields = {k: v for k, v in locals().items() if k != 'self'}
        self.block = None
        super(Block, self).__init__(**fields)