import random
import hashlib
import time
from collections import defaultdict

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.balance = 100  # Initial balance for all nodes

    def receive_transaction(self, transaction):
        print(f"{self.node_id} received transaction: {transaction}")

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = {}
        self.difficulty = 3
        self.spent_inputs = set()  # Track spent coins to detect double-spending

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
        tx_key = (sender, amount)  # Unique key to detect double-spending

        # Detect and prevent double-spending
        if tx_key in self.spent_inputs:
            print(f"Double-spending detected! Transaction {tx_key} is not allowed.")
            return

        if sender in self.nodes and self.nodes[sender].balance >= amount:
            transaction = {'sender': sender, 'receiver': receiver, 'amount': amount}
            self.pending_transactions.append(transaction)
            self.spent_inputs.add(tx_key)  # Mark this input as spent
            self.nodes[sender].balance -= amount
            print(f"Transaction added: {transaction}")
        else:
            print(f"Transaction from {sender} to {receiver} failed: Insufficient balance or invalid node.")

    def hash(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def mine_block_nonce(self):
        print("Mining block...")
        nonce = 0
        while True:
            guess = f"{nonce}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash[:self.difficulty] == "0" * self.difficulty:
                return nonce
            nonce += 1

    def print_chain(self):
        for block in self.chain:
            print(block)

    def print_balances(self):
        print("\n--- Node Balances ---")
        for node_id, node in self.nodes.items():
            print(f"{node_id}: {node.balance} coins")

# Add initial nodes
def add_initial_nodes(blockchain, num_nodes=5):
    for i in range(1, num_nodes + 1):
        node_id = f"node_{i}"
        blockchain.nodes[node_id] = Node(node_id)
        print(f"Added node: {node_id}")

# Create and add a new block, with double-spending detection
def create_and_add_new_block_with_detection(blockchain):
    if blockchain.pending_transactions:
        print("\nChecking for double-spending before adding block...")
        if detect_double_spending_in_block(blockchain.pending_transactions):
            print("Block creation aborted due to detected double-spending.")
            return

        new_block = blockchain.create_block(blockchain.pending_transactions)
        blockchain.add_block(new_block)
        blockchain.pending_transactions.clear()
        print("\nNew block successfully created.")
    else:
        print("\nNo pending transactions to add.")

# Detect double-spending within a block
def detect_double_spending_in_block(transactions):
    seen_inputs = set()
    for tx in transactions:
        tx_key = (tx['sender'], tx['amount'])
        if tx_key in seen_inputs:
            print(f"Double-spending detected! Conflicting transaction: {tx}")
            return True
        seen_inputs.add(tx_key)
    return False

# Double-spending attack simulation
def double_spending_attack(blockchain):
    print("\n--- Double-Spending Attack Initiated ---")
    
    attacker = "attacker_node"
    blockchain.nodes[attacker] = Node(attacker)
    blockchain.nodes[attacker].balance = 50  # Set attacker balance

    # Attacker sends two conflicting transactions
    print("Attacker sends two conflicting transactions.")
    blockchain.add_transaction(attacker, "node_1", 50)  # Transaction 1
    blockchain.add_transaction(attacker, "node_2", 50)  # Conflicting Transaction 2

    # Attempt to add both transactions into the blockchain
    create_and_add_new_block_with_detection(blockchain)

# Main simulation loop
def main():
    blockchain = Blockchain()
    blockchain.create_genesis_block()

    # Add initial nodes
    add_initial_nodes(blockchain, num_nodes=5)

    print("\nWelcome to the Blockchain Simulation!")
    blockchain.print_balances()

    while True:
        print("\n--- Main Menu ---")
        print("1. Add a transaction")
        print("2. Create and add new block")
        print("3. Trigger double-spending attack")
        print("4. Print blockchain")
        print("5. Print node balances")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            sender = input("Enter sender node: ")
            receiver = input("Enter receiver node: ")
            amount = int(input("Enter amount to send: "))
            blockchain.add_transaction(sender, receiver, amount)

        elif choice == '2':
            create_and_add_new_block_with_detection(blockchain)

        elif choice == '3':
            double_spending_attack(blockchain)

        elif choice == '4':
            print("\n--- Blockchain State ---")
            blockchain.print_chain()

        elif choice == '5':
            blockchain.print_balances()

        elif choice == '6':
            print("Exiting the simulation. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the simulation
if __name__ == "__main__":
    main()
