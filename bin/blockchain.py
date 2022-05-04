import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        # Creates/init block

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Resets current transactions

        self.current_transactions = []

        # Append block to the chain and return it

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # Sender and recipient are strings, addresses

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        # Simple PoW algorithm
        # Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        # p is the previous proof, and p' is the new proof
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof

    @staticmethod
    def hash(block):
        # Creates SHA-256 hash of a Block
        # Block is a <dict> param
        
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        # Does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
        
    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

