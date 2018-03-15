from time import time
from unittest import TestCase
import numpy as np

from blockchain.Block import Block
from blockchain.VoteBlockChain import VoteBlockChain


class TestVoteBlockChain(TestCase):
    def setUp(self):
        self.vote_chain = VoteBlockChain()

    def test_adding_block(self):
        self.vote_chain.add_block(proof_of_work=True, previous_hash='test123')
        self.assertEqual(len(self.vote_chain.blocks), 1)

    def get_random_block(self, block_number=None, prevhash=None):
        block = {
            'number': block_number if block_number is not
                                      None else np.random.randint(2000),
            'timestamp': time(),
            'transactions': np.random.randint(2000),
            'proof': True,
            'prevhash': prevhash if prevhash is not None else b'\x00' * 32,
        }
        block_object = Block(block['timestamp'],
                             block['number'],
                             block['prevhash'])
        return block_object

    def test_block_hash(self):
        hash_binary = self.vote_chain.hash(self.get_random_block())
        self.assertEqual(len(hash_binary), 32)

    def test_persistance_block_to_database(self):
        self.generate_blocks()


    def generate_blocks(self):
        blocks_number = 20
        prevhash = b'\x00' * 32
        for i in range(blocks_number):
            block = self.get_random_block(i, prevhash)
            signed_block = self.vote_chain.add_block(block)
            prevhash = signed_block['prevhash']
        self.assertEqual(len(self.vote_chain.blocks), 20)