#!/bin/bash
# Short Script for Testing the Distributed Banking System Project

echo "===== Starting Short Test Script for Banking System ====="

echo "[1/5] Creating a new account for Tim (account 1078) with an initial deposit of 500"
python3 client.py Tim create_account 1078 500
sleep 1

echo "[2/5] Depositing 300 into Alice's account (1001)"
python3 client.py Alice deposit 1001 300
sleep 1

echo "[3/5] Withdrawing 200 from Bob's account (1003)"
python3 client.py Bob withdraw 1003 200
sleep 1

echo "[4/5] Transferring 150 from Charlie's account to Ivan's account (target account 1015)"
python3 client.py Charlie transfer_to 1015 150
sleep 1

echo "[5/5] Displaying transaction history for Alice's account (1001)"
python3 client.py Alice show_history 1001
sleep 1

echo "===== Short Test Script Completed ====="
