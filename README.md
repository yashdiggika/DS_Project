# Distributed System Project: ABC Bank Client-Server Simulation

## 1. Overview

This project simulates a distributed banking system using a client-server architecture. The server represents ABC Bank, handling various transactions from clients that connect via TCP sockets. The goal is to demonstrate key concepts in distributed systems, such as concurrency, synchronization, and network communication, and to provide a robust, testable system for educational purposes. This project was developed as the final project for CMSC 421 and includes several enhancements beyond the base requirements.

## 2. Project Structure

The repository includes the following files:
- **server.py**:  
  The main server application. It maintains account data, processes transactions (deposit, withdraw, transfer, loan payments), and uses mutex locks (`threading.Lock()`) to ensure thread-safe operations. Additional features include logging, interest calculation for loan accounts, and the ability to filter transaction histories.

- **client.py**:  
  The client application that parses command-line arguments using `argparse`, implements retry logic for robust connections, and uses `colorama` to print colored output indicating success or error.

- **run_bank.sh**:  
  A bash script that opens multiple terminal windows and simulates many concurrent client transactions. It includes echo statements to log which command is executing and has an optional dynamic testing loop for stress-testing.

- **short_script.sh**:  
  A lightweight bash script for sequential testing of key operations. It runs a series of client commands one after another to quickly verify core functionalities.

- **config.json** (optional):  
  A configuration file containing parameters such as the server port, interest rate, and auto-interest application interval. If this file is absent, default values are used.

- **README.md**:  
  This file, providing an overview, instructions, and details about the project.

## 3. Environment Setup

### A. Setting Up Your Debian Environment

This project is designed to run on a Debian Linux system. It is recommended to use a virtual machine (e.g., via UTM on Apple Silicon or VirtualBox on x86) to ensure compatibility with the grading environment.

1. **Start Your Debian VM**:  
   Boot into your Debian system using your virtualization tool.

2. **Open the Terminal**:  
   Use the Terminal application (you can usually open it via the applications menu or by pressing `Ctrl+Alt+T`).

3. **Install Required Packages**:  
   In the terminal, run the following commands:
   ```bash
   sudo apt update
   sudo apt install python3-pip git -y
   pip3 install tabulate colorama
