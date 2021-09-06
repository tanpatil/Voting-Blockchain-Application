"""
This file contains the building blocks of the blocks of the blockchain

We use JSON to store the data and a SHA256 hash to compute the hash of the data
"""



from hashlib import sha256
import json


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        """This function initialises the block of the blockchain using the regular concept

        Args:
            index ([type]): Index number of the block
            transactions ([type]): The Transactions to be stored in the given block
            timestamp ([type]): The timestamp of the given block
            previous_hash ([type]): The hash of the previous block to store
            nonce (int, optional): The number only used once. The nonce is to maintain uniqueness, making it hard to regenerate, which gives the blockchain the power it needs. Defaults to 0.
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()