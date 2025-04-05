#!/usr/bin/env python3
import sys
import socket
import time
import argparse
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output.
init(autoreset=True)

# Set up host and port (using the machine's hostname and port 9876)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9876
ADDR = (HOST, PORT)

def send_request(user_input, retries=3, delay=2):
    """
    Connects to the server, sends the request formatted as a string,
    receives the response (handling multi-chunk messages ending with "END"),
    and returns the full response.
    
    Implements retry logic if the connection fails.
    """
    attempt = 0
    while attempt < retries:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(ADDR)
            break
        except socket.error as e:
            print(Fore.YELLOW + f"Connection failed, retrying in {delay} seconds... (Attempt {attempt+1}/{retries})")
            attempt += 1
            time.sleep(delay)
    else:
        print(Fore.RED + "Failed to connect to the server after multiple attempts.")
        sys.exit(1)

    # Format and send the user input as a request string
    request_str = " ".join(f"{key}={value}" for key, value in user_input.items())
    client_socket.send(request_str.encode())

    # Receive data in chunks until we see the "END" marker
    response = ""
    while True:
        chunk = client_socket.recv(1024).decode()
        if "END" in chunk:
            response += chunk.replace("END", "")
            break
        response += chunk

    client_socket.close()
    return response

def main():
    # Use argparse for enhanced CLI and help messages.
    parser = argparse.ArgumentParser(description="Distributed System Project Client")
    parser.add_argument("user", help="Username for the transaction")
    parser.add_argument("command", help="Command to execute (e.g., deposit, withdraw, create_account, etc.)")
    parser.add_argument("acct_num", nargs="?", default=0, type=int, help="Account number (default: 0)")
    parser.add_argument("amount", nargs="?", default=0, type=int, help="Transaction amount (default: 0)")
    args = parser.parse_args()

    # Prepare the request data as a dictionary.
    user_input = {
        'user': args.user,
        'command': args.command,
        'acct_num': args.acct_num,
        'amount': args.amount
    }

    # Send the request to the server and retrieve the response.
    response = send_request(user_input)

    # Determine the color of the output:
    # If the response indicates an error (e.g., "error", "insufficient", "denied"), print in red.
    if any(err in response.lower() for err in ["error", "insufficient", "denied", "failed"]):
        print(Fore.RED + "******************************************************************")
        print(response)
        print("******************************************************************")
    else:
        print(Fore.GREEN + "******************************************************************")
        print(response)
        print("******************************************************************")

if __name__ == "__main__":
    main()
