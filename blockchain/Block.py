import rlp
from ethereum import utils

GENESIS_PREVHASH=b'\x00' * 32

class Block(rlp.Serializable):
    FIELDS = ['prevhash', 'timestamp', 'number']

    def __init__(self,
                 nonce,
                 number,
                 prevhash=GENESIS_PREVHASH,
                 transactions=None):
        fields = {k: v for k, v in locals().items() if k != 'self'}
        self.block = None
        self.transactions = transactions or []
        super(Block, self).__init__(**fields)


    @property
    def hash(self):
        """The binary block hash"""
        return utils.sha3(rlp.encode(self))