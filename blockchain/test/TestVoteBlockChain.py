from time import time
from unittest import TestCase
import numpy as np
import os

from blockchain.Database import Database
from blockchain.VoteBlockChain import VoteBlockChain

DEFAULT_PREVHASH = b'\x00' * 32
VOTE_DB = 'test_vote_db.pkl'

class TestVoteBlockChain(TestCase):
    def setUp(self):
        self.vote_chain = VoteBlockChain(database=Database(VOTE_DB))

    def tearDown(self):
        if os.path.exists(VOTE_DB):
            os.remove(VOTE_DB)

    def test_adding_block(self):
        self.vote_chain.add_block(self.get_random_block())
        self.assertEqual(self.vote_chain.blocks_count, 1)

    def get_random_block(self, block_number=None, prevhash=None):
        block = {
            'number': block_number if block_number is not
                                      None else np.random.randint(2000),
            'timestamp': time(),
            'transactions': np.random.randint(2000),
            'proof': True,
            'prevhash': prevhash if prevhash is not None else DEFAULT_PREVHASH,
        }
        return block

    def test_block_hash(self):
        dict_block = self.get_random_block()
        block = self.vote_chain.get_block_from_dict(dict_block)
        hash_binary = self.vote_chain.hash(block)
        self.assertEqual(len(hash_binary), 32)

    def test_persistance_block_to_database(self):
        self.generate_blocks()

    def generate_blocks(self):
        blocks_number = 20
        for i in range(blocks_number):
            block = self.get_random_block(i)
            self.vote_chain.add_block(block)
        self.assertEqual(self.vote_chain.blocks_count, 20)