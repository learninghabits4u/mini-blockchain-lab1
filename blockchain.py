"""
Minimal blockchain for lab:
- Block with timestamp, transactions, previous_hash, nonce
- Proof-of-Work (difficulty = number of leading zeros)
- Pending transaction pool and mining reward
- Chain validation and tamper detection
"""

import hashlib, json, time
from datetime import datetime

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None, nonce=0):
        self.index = index
        self.transactions = transactions  # list of dicts
        self.previous_hash = previous_hash
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, difficulty=4, mining_reward=50):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = mining_reward

    def create_genesis_block(self):
        return Block(0, [{"genesis": True}], "0", timestamp=datetime.utcnow().isoformat())

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, tx):
        # minimal validation: tx must have from,to,amount
        if not all(k in tx for k in ("from", "to", "amount")):
            raise ValueError("Transaction must include from, to, amount")
        self.pending_transactions.append(tx)

    def proof_of_work(self, block):
        target = "0" * self.difficulty
        while True:
            block.hash = block.calculate_hash()
            if block.hash.startswith(target):
                return block.hash
            block.nonce += 1

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return None
        # include a mining reward transaction
        reward_tx = {"from": "network", "to": miner_address, "amount": self.mining_reward}
        block_txs = self.pending_transactions[:]  # snapshot
        block_txs.append(reward_tx)
        new_block = Block(self.get_last_block().index + 1, block_txs, self.get_last_block().hash)
        print(f"Mining block {new_block.index} with {len(block_txs)} txs ... (difficulty={self.difficulty})")
        start = time.time()
        self.proof_of_work(new_block)
        elapsed = time.time() - start
        self.chain.append(new_block)
        self.pending_transactions = []  # cleared after mining
        print(f"Block {new_block.index} mined: {new_block.hash} (nonce={new_block.nonce}, time={elapsed:.2f}s)")
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            # check hash integrity
            if current.hash != current.calculate_hash():
                print(f"Invalid hash at block {current.index}")
                return False
            if current.previous_hash != prev.hash:
                print(f"Broken link between {prev.index} and {current.index}")
                return False
            # check proof-of-work
            if not current.hash.startswith("0" * self.difficulty):
                print(f"Block {current.index} does not meet PoW difficulty")
                return False
        return True

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.get("from") == address:
                    balance -= tx.get("amount", 0)
                if tx.get("to") == address:
                    balance += tx.get("amount", 0)
        # pending txs do not affect confirmed balance
        return balance

    def show_chain(self):
        for b in self.chain:
            print(f"--- Block {b.index} ---")
            print(f"Timestamp: {b.timestamp}")
            print(f"Previous: {b.previous_hash}")
            print(f"Nonce: {b.nonce}")
            print(f"Hash: {b.hash}")
            print("Transactions:")
            for t in b.transactions:
                print(" ", t)
            print()

#Run when invoked directly
if __name__ == "__main__":
    bc = Blockchain(difficulty=4)
    # add sample transactions
    bc.add_transaction({"from": "alice", "to": "bob", "amount": 10})
    bc.add_transaction({"from": "bob", "to": "charlie", "amount": 2})
    # mine (miner gets reward)
    bc.mine_pending_transactions("miner1")
    # more transactions
    bc.add_transaction({"from": "charlie", "to": "alice", "amount": 1})
    bc.mine_pending_transactions("miner1")
    # show chain & balances
    bc.show_chain()
    print("Balances:")
    for name in ("alice","bob","charlie","miner1"):
        print(name, bc.get_balance_of_address(name))
    print("Valid:", bc.is_chain_valid())

