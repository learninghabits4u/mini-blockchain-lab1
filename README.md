# Mini Blockchain Lab 1

This repo contains a **minimal blockchain implementation in Python** for learning purposes.

## Features
- Block with timestamp, transactions, previous hash, nonce
- Proof-of-Work mining (adjustable difficulty)
- Transaction pool + mining reward
- Chain validation and tamper detection
- Balance calculation per address

## Prerequisites
- Python 3.8+  
- Ubuntu/Debian or Windows WSL recommended  

On Ubuntu:
```bash
sudo apt update && sudo apt install -y python3 git
```
Create a working folder and virtualenv (optional):
```bash
mkdir ~/blockchain-week5 && cd ~/blockchain-week5
python3 -m venv venv
source venv/bin/activate
```
Make script executable and run it:
```bash
chmod +x blockchain.py
python3 blockchain.py
```
Redirect output to a file
```bash
python3 blockchain.py > run-output.txt
```
### Testing with this Mini Blockchain
- Tampering demonstration
- Open a Python REPL in the same folder:
```bash
python3
```
Import and inspect the chain:
```bash
from blockchain import Blockchain
bc = Blockchain(difficulty=4)
# repeat the demo sequence
bc.add_transaction({"from":"alice","to":"bob","amount":10})
bc.mine_pending_transactions("miner1")
bc.add_transaction({"from":"bob","to":"charlie","amount":1})
bc.mine_pending_transactions("miner1")
print("Valid before tamper:", bc.is_chain_valid())
# tamper with block 1:
bc.chain[1].transactions[0]["amount"] = 9999
print("Valid after tamper:", bc.is_chain_valid())
```
Result: is_chain_valid() should return False after tampering
### Another Quick Live Demo
Run this command for short live demo
```bash
python3 - <<'PY'
from blockchain import Blockchain
bc = Blockchain(difficulty=3)
bc.add_transaction({"from":"alice","to":"bob","amount":5})
bc.mine_pending_transactions("miner1")
bc.show_chain()
print("Valid:", bc.is_chain_valid())
PY
```

