from time import time
import rlp
from ethereum import utils

DEFAULT_CONFIG = {
    'CONSENSUS_STRATEGY': 'vote'
}


class VoteBlockChain(object):
    def __init__(self, genesis_block={}, concensus_strategy='vote',
                 database=None):
        DEFAULT_CONFIG.update({
            'CONSENSUS_STRATEGY': concensus_strategy
        })
        self.database = database if database is not None else None
        self.blocks = [] if self.database is None \
            else self.database.get_blocks()
        self.state = None
        self.current_block_transactions = []

    def add_block(self, proof_of_work, previous_hash=None):
        block = {
            'index': len(self.blocks) + 1,
            'timestamp': time(),
            'transactions': self.current_block_transactions,
            'proof': proof_of_work,
            'prevhash': previous_hash or self.hash(self.blocks[-1]),
        }

        # Reset the current list of transactions
        self.current_block_transactions = []

        self.blocks.append(block)
        # TODO persist blocks to database file
        return block

    @staticmethod
    def hash(block):
        return utils.sha3(rlp.encode(block))
