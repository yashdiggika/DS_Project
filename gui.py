#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import time
import threading

# Server connection settings (ensure these match your server configuration)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9876
ADDR = (HOST, PORT)

def send_request(user_input, retries=3, delay=2):
    """Send a request to the server and return the response."""
    attempt = 0
    response = ""
    while attempt < retries:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(ADDR)
            break
        except socket.error:
            attempt += 1
            time.sleep(delay)
    else:
        return "Failed to connect to the server after several attempts."
    
    # Format the request string (e.g., "user=Alice command=deposit acct_num=1001 amount=500")
    request_str = " ".join(f"{key}={value}" for key, value in user_input.items())
    client_socket.send(request_str.encode())
    
    # Receive the response until we see the "END" marker
    while True:
        chunk = client_socket.recv(1024).decode()
        if "END" in chunk:
            response += chunk.replace("END", "")
            break
        response += chunk
    client_socket.close()
    return response

def send_command():
    """Collect user inputs, send the request in a separate thread, and display the response."""
    user = entry_user.get().strip()
    command = entry_command.get().strip()
    acct_num = entry_acct.get().strip() or "0"
    amount = entry_amount.get().strip() or "0"
    
    # Prepare the data dictionary to match the expected format
    user_input = {
        'user': user,
        'command': command,
        'acct_num': acct_num,
        'amount': amount,
    }
    
    # Use a thread to avoid freezing the GUI while waiting for the server response
    def thread_function():
        resp = send_request(user_input)
        # Update the response text widget (in the main thread)
        text_response.config(state=tk.NORMAL)
        text_response.delete("1.0", tk.END)
        text_response.insert(tk.END, resp)
        text_response.config(state=tk.DISABLED)
    
    threading.Thread(target=thread_function, daemon=True).start()

# Create the main Tkinter window
root = tk.Tk()
root.title("ABC Bank Client UI")

# Create a frame with padding
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Username field
ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
entry_user = ttk.Entry(frame, width=20)
entry_user.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Command field
ttk.Label(frame, text="Command:").grid(row=1, column=0, sticky=tk.W)
entry_command = ttk.Entry(frame, width=20)
entry_command.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Account Number field
ttk.Label(frame, text="Account Number:").grid(row=2, column=0, sticky=tk.W)
entry_acct = ttk.Entry(frame, width=20)
entry_acct.grid(row=2, column=1, sticky=(tk.W, tk.E))

# Amount field
ttk.Label(frame, text="Amount:").grid(row=3, column=0, sticky=tk.W)
entry_amount = ttk.Entry(frame, width=20)
entry_amount.grid(row=3, column=1, sticky=(tk.W, tk.E))

# Send Request button
button_send = ttk.Button(frame, text="Send Request", command=send_command)
button_send.grid(row=4, column=0, columnspan=2, pady=10)

# Response display area
ttk.Label(frame, text="Response:").grid(row=5, column=0, sticky=tk.W)
text_response = scrolledtext.ScrolledText(frame, width=50, height=10, state=tk.DISABLED)
text_response.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Start the Tkinter event loop
root.mainloop()
