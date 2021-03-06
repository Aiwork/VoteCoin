import logging
import time

import rlp
from ethereum import utils
from rlp.utils_py3 import encode_hex

GENESIS_PREVHASH = b'\x00' * 32


class Block(rlp.Serializable):

    def __init__(self,
                 nonce='',
                 number=0,
                 prevhash=GENESIS_PREVHASH,
                 transactions=[]):
        fields = {k: v for k, v in locals().items() if k != 'self'}
        self.block = None
        self.number = number
        self.prevhash = prevhash
        self.timestamp = nonce
        self.proof = True
        self.transactions = transactions
        super(Block, self).__init__(
            transactions=transactions,
        )

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
        """Two blocks are equal iff they have the same hash."""
        return isinstance(other, Block) and self.hash == other.hash

    def __hash__(self):
        return utils.big_endian_to_int(self.hash)

    def __repr__(self):
        return '<%s(#%d %s)>' % (self.__class__.__name__, self.number,
                                 encode_hex(self.hash)[:8])

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self, block_number=None):
        return {
            'transactions': self.transactions,
            'number': self.number if block_number is None else block_number,
            'timestamp': time.time(),
            'prevhash': self.hash,
            'proof': self.proof,
        }

    def add_transaction(self, transaction):
        logging.debug('Adding transaction to head block transaction={}'.format(transaction))
        self.transactions.append(transaction.to_dict())