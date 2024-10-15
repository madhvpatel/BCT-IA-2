import random
import hashlib
import time
from collections import defaultdict

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.balance = 100  # All nodes start with 100 coins
        self.stake = 0      # Default stake amount is 0

    def receive_transaction(self, transaction):
        print(f"{self.node_id} received transaction: {transaction}")

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = {}  # Store node_id -> Node object
        self.difficulty = 3  # Mining difficulty
        self.minimum_stake = 20  # Minimum stake to participate

    def create_genesis_block(self):
        genesis_block = self.create_block("Genesis Block")
        self.chain.append(genesis_block)

    def create_block(self, transactions):
        block = {
            'index': len(self.chain) + 1,
            'transactions': transactions,
            'previous_hash': self.hash(self.chain[-1]) if self.chain else '0',
            'nonce': self.mine_block_nonce()
        }
        return block

    def add_block(self, block):
        self.chain.append(block)
        print(f"\nBlock {block['index']} mined and added!")

    def add_transaction(self, sender, receiver, amount):
        if self.is_eligible_for_transaction(sender):
            if sender in self.nodes and self.nodes[sender].balance >= amount:
                transaction = {'sender': sender, 'receiver': receiver, 'amount': amount}
                self.pending_transactions.append(transaction)
                self.nodes[sender].balance -= amount
                print(f"Transaction added: {transaction}")
                self.gossip_transaction(transaction)
            else:
                print(f"Transaction from {sender} to {receiver} failed: Insufficient balance.")
        else:
            print(f"Transaction from {sender} blocked: Insufficient stake.")

    def is_eligible_for_transaction(self, node_id):
        """Check if a node has enough stake to participate."""
        return self.nodes[node_id].stake >= self.minimum_stake

    def hash(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def mine_block_nonce(self):
        print("Mining block...")
        nonce = 0
        while True:
            guess = f"{nonce}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash[:self.difficulty] == "0" * self.difficulty:
                return nonce  # Found a valid nonce
            nonce += 1

    def gossip_transaction(self, transaction):
        print("\nGossiping transaction across the network...")
        time.sleep(1)  # Simulate gossip delay
        for node_id in self.nodes:
            if random.random() < 0.7:  # Random chance to propagate
                peers = random.sample(list(self.nodes.keys()), 2)
                for peer in peers:
                    if peer != node_id:
                        self.nodes[peer].receive_transaction(transaction)

    def print_chain(self):
        for block in self.chain:
            print(block)

    def print_balances_and_stakes(self):
        print("\n--- Node Balances and Stakes ---")
        for node_id, node in self.nodes.items():
            print(f"{node_id}: {node.balance} coins, {node.stake} stake")

# Function to add initial nodes
def add_initial_nodes(blockchain, num_nodes=5):
    for i in range(1, num_nodes + 1):
        node_id = f"node_{i}"
        blockchain.nodes[node_id] = Node(node_id)
        blockchain.nodes[node_id].stake = random.randint(10, 30)  # Assign random stake
        print(f"Added initial node: {node_id} with stake {blockchain.nodes[node_id].stake}")

# Sybil Attack Simulation
def sybil_attack(blockchain):
    print("\n--- Sybil Attack Initiated ---")
    num_sybil_nodes = int(input("Enter the number of fake (Sybil) nodes to create: "))

    # Create fake nodes with low stake
    for i in range(num_sybil_nodes):
        sybil_node_id = f"sybil_node_{i+1}"
        blockchain.nodes[sybil_node_id] = Node(sybil_node_id)
        blockchain.nodes[sybil_node_id].stake = random.randint(0, 10)  # Low stake for Sybil nodes
        print(f"Created Sybil node: {sybil_node_id} with stake {blockchain.nodes[sybil_node_id].stake}")

    # Sybil nodes attempt transactions
    print("\nSybil nodes attempting to perform transactions...")
    for sybil_node_id in blockchain.nodes:
        if sybil_node_id.startswith("sybil"):
            blockchain.add_transaction(sybil_node_id, "node_1", random.randint(1, 5))

# Function to create and add a new block
def create_and_add_new_block(blockchain):
    if blockchain.pending_transactions:
        new_block = blockchain.create_block(blockchain.pending_transactions)
        blockchain.add_block(new_block)
        blockchain.pending_transactions.clear()
        print("\nNew block successfully created and added to the blockchain.")
    else:
        print("\nNo pending transactions to include in the new block.")

# Main Simulation Loop
def main():
    blockchain = Blockchain()
    blockchain.create_genesis_block()

    # Add initial nodes
    add_initial_nodes(blockchain, num_nodes=5)

    print("\nWelcome to the Blockchain Simulation with PoS-based Sybil Prevention!")
    blockchain.print_balances_and_stakes()

    while True:
        print("\n--- Main Menu ---")
        print("1. Add a transaction")
        print("2. Create and add new block")
        print("3. Trigger Sybil attack")
        print("4. Print blockchain")
        print("5. Print node balances and stakes")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            sender = input("Enter sender node: ")
            receiver = input("Enter receiver node: ")
            amount = int(input("Enter amount to send: "))
            blockchain.add_transaction(sender, receiver, amount)

        elif choice == '2':
            create_and_add_new_block(blockchain)

        elif choice == '3':
            sybil_attack(blockchain)

        elif choice == '4':
            print("\n--- Blockchain State ---")
            blockchain.print_chain()

        elif choice == '5':
            blockchain.print_balances_and_stakes()

        elif choice == '6':
            print("Exiting the simulation. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the simulation
if __name__ == "__main__":
    main()
