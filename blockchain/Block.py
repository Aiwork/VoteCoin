import rlp
from ethereum import utils
from ethereum.utils import hash32
from rlp.utils_py3 import encode_hex

GENESIS_PREVHASH = b'\x00' * 32


class Block(rlp.Serializable):
    # fields = (
    #     ('prevhash', hash32),
    #     ('nonce', float),
    #     ('transactions', list),
    # )

    def __init__(self,
                 nonce='',
                 number=0,
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

    def un_hash(self, key):
        return utils.sha3rlp(rlp.decode(key))

    @property
    def transaction_count(self):
        return len(self.transactions)

    def __getattribute__(self, name):
        try:
            return rlp.Serializable.__getattribute__(self, name)
        except AttributeError:
            return getattr(self.header, name)

    def __eq__(self, other):
        """Two blockheader are equal iff they have the same hash."""
        return isinstance(other, Block) and self.hash == other.hash

    def __hash__(self):
        return utils.big_endian_to_int(self.hash)

    def __repr__(self):
        return '<%s(#%d %s)>' % (self.__class__.__name__, self.number,
                                 encode_hex(self.hash)[:8])

    def __ne__(self, other):
        return not self.__eq__(other)