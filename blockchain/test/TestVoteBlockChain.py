from unittest import TestCase
import numpy as np
import os

from blockchain.Block import Block
from blockchain.Database import Database
from blockchain.Transaction import Transaction
from blockchain.VoteBlockChain import VoteBlockChain

DEFAULT_PREVHASH = b'\x00' * 32
VOTE_DB = 'test_vote_db.pkl'


def get_transaction(index):
    return Transaction(meta={index: index}).to_dict()


def get_transactions(max_transactions):
    return [get_transaction(i) for i in range(max_transactions)]


def get_random_block(block_number=None, prevhash=None):
    block_number = block_number if block_number is not None else np.random.randint(
        2000)
    block = Block().to_dict(block_number=block_number)
    block['transactions'] = get_transactions(2000)
    return block

class TestVoteBlockChain(TestCase):
    def setUp(self):
        self.vote_chain = VoteBlockChain(database=Database(VOTE_DB))

    def tearDown(self):
        if os.path.exists(VOTE_DB):
            os.remove(VOTE_DB)

    def get_transaction(self, index):
        return Transaction(meta={index: index}).to_dict()

    def get_transactions(self, max_transactions):
        return [self.get_transaction(i) for i in range(max_transactions)]

    def get_random_block(self, block_number=None, prevhash=None):
        block_number = block_number if block_number is not None else np.random.randint(2000)
        block = Block().to_dict(block_number=block_number)
        block['transactions'] = self.get_transactions(2000)
        return block

    def generate_blocks(self):
        blocks_number = 20
        for i in range(blocks_number):
            block = self.get_random_block(i)
            self.vote_chain.add_block(block)
        self.assertEqual(self.vote_chain.blocks_count, 20)

    def test_adding_block(self):
        self.vote_chain.add_block(self.get_random_block())
        self.assertEqual(self.vote_chain.blocks_count, 1)

    def test_block_hash(self):
        dict_block = self.get_random_block()
        block = self.vote_chain.get_block_from_dict(dict_block)
        hash_binary = self.vote_chain.hash(block)
        self.assertEqual(len(hash_binary), 32)

    def test_persistance_block_to_database(self):
        self.generate_blocks()

    def test_get_block(self):
        block = self.append_random_block()
        block_found = self.vote_chain.get_block(block.hash)
        self.assertEqual(block.hash, block_found.hash)

    def append_random_block(self):
        block_dict = self.get_random_block()
        block = self.vote_chain.add_block(block_dict)
        return block

    def test_get_chain(self):
        length_chain = 10
        for i in range(length_chain):
            self.append_random_block()
        chain = self.vote_chain.get_chain()
        self.assertEqual(len(self.vote_chain.get_chain()), 10)
        self.assertEqual(len(chain), 10)
        for block, i in zip(chain, range(len(chain)+1)):
            if i is 0:
                continue
            self.assertEqual(block.hash, chain[i].hash)

    def test_get_head_block(self):
        block = self.append_random_block()
        block_found = self.vote_chain.get_head_block()
        self.assertEqual(block.hash, block_found.hash)

    def test_append_transaction(self):
        block = self.append_random_block()
        transaction = Transaction(meta={'vote_value': 'ron_huldai'})
        self.vote_chain.append_transaction(transaction)
        head_block = self.vote_chain.get_head_block()
        print('head_block.transactions={}'.format(head_block.transactions))
        self.assertEqual(len(head_block.transactions), 1)