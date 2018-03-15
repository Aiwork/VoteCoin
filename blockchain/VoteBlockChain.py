from time import time
import rlp
from ethereum import utils
from sklearn.externals import joblib

from blockchain.Block import Block
from blockchain.Database import Database

DEFAULT_CONFIG = {
    'CONSENSUS_STRATEGY': 'vote',
    'database_filename': 'vote_db.pkl'
}

DEFAULT_PREVHASH = b'\x00' * 32


class VoteBlockChain(object):
    def __init__(self, genesis_block={}, concensus_strategy='vote',
                 database=None):
        DEFAULT_CONFIG.update({
            'CONSENSUS_STRATEGY': concensus_strategy
        })
        self.database = database if database is not None \
            else Database(DEFAULT_CONFIG['database_filename'])
        self.blocks_count = 0 if self.database is None \
            else self.database.get_index_count()
        self.state = None
        self.current_block_transactions = []
        self.head_hash = DEFAULT_PREVHASH \
            if 'hash' not in genesis_block else genesis_block['hash']

    def add_block(self, block_dict):
        block_dict.update({
            'number': self.blocks_count + 1,
            'timestamp': time(),
            'prevhash': self.hash(self.head_hash)
        })
        block = self.get_block_from_dict(block_dict)
        # Reset the current list of transactions
        self.current_block_transactions = []
        self.blocks_count += 1
        self.persist_block(block)

        return block

    def get_block_from_dict(self, block_dict):
        return Block(block_dict['timestamp'],
                     block_dict['number'],
                     block_dict['prevhash'])

    @staticmethod
    def hash(block):
        return utils.sha3(rlp.encode(block))

    def persist_block(self, block):
        block_num = b'block:%d' % self.blocks_count
        self.database.put(block_num, block.hash)
        self.database.put('head_hash', block.hash)
        self.database.commit()
