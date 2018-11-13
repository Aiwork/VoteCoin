import rlp
from ethereum import utils
from rlp.sedes import big_endian_int, lists
from rlp.utils_py3 import encode_hex

GENESIS_PREVHASH = b'\x00' * 32


class Transaction(rlp.Serializable):

    def __init__(self,
                 nonce='',
                 number=0,
                 prevhash=GENESIS_PREVHASH,
                 meta=None):
        fields = {k: v for k, v in locals().items() if k != 'self'}
        self.meta = meta or {}
        self.number = number
        super(Transaction, self).__init__(**fields)

    @property
    def hash(self):
        """The binary block hash"""
        return utils.sha3(rlp.encode(self))

    def un_hash(self, key):
        return utils.sha3rlp(rlp.decode(key))

    def __getattribute__(self, name):
        try:
            return rlp.Serializable.__getattribute__(self, name)
        except AttributeError:
            return getattr(self.header, name)

    def __eq__(self, other):
        """Two blocks are equal iff they have the same hash."""
        return isinstance(other, Transaction) and self.hash == other.hash

    def __hash__(self):
        return utils.big_endian_to_int(self.hash)

    def __repr__(self):
        return '<%s(#%d %s)>' % (self.__class__.__name__, self.number,
                                 encode_hex(self.hash)[:8])

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return {
            'meta': self.meta,
            'hash': self.hash,
            'number': self.number
        }