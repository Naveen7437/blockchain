import json
import time
from hashlib import sha256


# Any block created will take the hash of previous generated block and
# current data and will generate a hash for it

class Block(object):
    def __init__(self, transactions, timestamp, prev_hash):
        self.transactions = transactions
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.hash = None

    def generate_hash(self):
        block_data = json.dumps(self.__dict__)
        self.hash = sha256(block_data.encode()).hexdigest()
        return self.hash


# BlockChain class which takes blocks one by one and creates a chain out
# of it using the prev_hash


class BlockChain(object):
    difficulty = 1

    def __init__(self):
        # this is reffered as the chain of the blocks

        self.pending_transaction = []

        self.chain = []

    def get_genesis_block(self):
        # this is the first block as the we don't have the prev_hash to
        # generated the hash of this block

        # as we don't have the data to create the hash, so using 0 values and
        # current datetime to generate the hash

        if self.chain:
            return False

        first_block = Block([], time.time(), 0)

        # first_hash = first_block.generate_hash()

        self.chain.append(first_block)

    @classmethod
    def get_last_block(cls):
        return cls.chain[-1]

    def proof_of_work(self, block):

        # If we change the previous block, we can re-compute the hashes of all
        #  the following blocks quite easily and create a different valid
        #  blockchain. To prevent this, we must make the task of calculating
        #  the hash difficult and random.

        # we add leading zeros to our hash
        # a nonce is a number that  we keep on updating until we get a
        # hash that satisfies our constraint.

        block.nonce = 0

        computed_hash = block.generate_hash()

        while not computed_hash.startswith('0'*self.difficulty):
            computed_hash = block.generate_hash()
            block.nonce += 1

        return computed_hash

    def add_new_block(self, block, proof):
        prev_hash = block.prev_hash
        last_block_hash = self.get_last_block.hash

        if prev_hash != last_block_hash:
            return False

        if not self._is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, hash):
        """
        we get the hash and now we are checking the hash provided is valid or
        not
        """
        if hash.startswith('0'*self.difficulty) and\
                block.generate_hash() == hash:
            return True

        return False

    @classmethod
    def add_transaction(self, transaction):
        self.pending_transaction.append(transaction)

    def mine(self):
        # if there is no pending transaction then there is nothing to mine
        if not self.pending_transaction:
            return False

        # create a new block

        # get the last block hash
        last_block_hash = self.get_last_block().hash

        new_block = Block(self.pending_transaction, time.time(), last_block_hash)

        proof = self.proof_of_work(new_block)

        self.add_new_block(new_block, proof)

        self.pending_transaction = []
        return new_block
