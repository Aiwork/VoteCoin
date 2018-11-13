import logging
from time import time

import itertools
import rlp
from ethereum import utils

from blockchain.Transaction import Transaction
from blockchain.Block import Block
from blockchain.Database import Database

DEFAULT_CONFIG = {
    'CONSENSUS_STRATEGY': 'vote',
    'database_filename': 'vote_db.pkl'
}

DEFAULT_PREVHASH = b'\x00' * 32
HEAD_HASH_NAME = 'head_hash'

class VoteBlockChain(object):
    def __init__(self, genesis_block={}, concensus_strategy='vote',
                 database=None):
        DEFAULT_CONFIG.update({
            'CONSENSUS_STRATEGY': concensus_strategy
        })
        self.database = database if database is not None \
            else Database(DEFAULT_CONFIG['database_filename'])
        self.blocks_count = 1 if self.database is None \
            else self.database.get_index_count()
        self.state = None
        self.current_block_transactions = []
        self.head_hash = DEFAULT_PREVHASH \
            if 'hash' not in genesis_block else genesis_block['hash']

    def add_block(self, block_dict):
        block_dict.update({
            'number': self.blocks_count + 1,
            'timestamp': time(),
            'prevhash': self.head_hash
        })
        block = self.get_block_from_dict(block_dict)
        # Reset the current list of transactions
        self.current_block_transactions = []
        self.blocks_count += 1
        self.persist_block(block)

        return block

    def get_block_from_dict(self, block_dict):
        return Block(nonce=block_dict['timestamp'],
                     number=block_dict['number'],
                     prevhash=block_dict['prevhash'])

    @staticmethod
    def hash(block):
        return utils.sha3(rlp.encode(block))

    def persist_block(self, block):
        block_num = b'block:%d' % self.blocks_count
        self.database.put(block_num, block.hash)
        self.database.put(block.hash, rlp.encode(block))
        self.database.put(HEAD_HASH_NAME, block.hash)
        self.database.commit()

    def get_block(self, blockhash):
        try:
            block_rlp = self.database.get(blockhash)
            return rlp.decode(block_rlp, Block)
        except Exception as e:
            logging.info('Failed to get'
                         ' block={hash} error={error}'.format(hash=blockhash,
                                                              error=e))
            return None

    def get_chain(self, frm=None, to=2 ** 63 - 1):
        if frm is None:
            frm = 1
            to = self.blocks_count + 1
        chain = []
        for i in itertools.islice(itertools.count(), frm, to):
            h = self.get_blockhash_by_number(i)
            if not h:
                return chain
            chain.append(self.get_block(h))
        return chain

    def get_blockhash_by_number(self, number):
        try:
            return self.database.get(b'block:%d' % number)
        except Exception:
            return None

    def get_head_block(self):
        block_hash = self.database.get(HEAD_HASH_NAME)
        return self.get_block(block_hash)

    def append_meta_transaction(self, meta):
        return self.append_transaction(Transaction(meta=meta))

    def append_transaction(self, transaction):
        logging.info('Applying block transactions')
        head_block = self.get_head_block()
        self.current_block_transactions.append(transaction.to_dict())
        logging.info('Checking delegation for vote block approval')
        head_block.add_transaction(transaction)
        self.persist_block(head_block)