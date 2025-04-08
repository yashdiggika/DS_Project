import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading

# Server address
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9876
ADDR = (HOST, PORT)

class BankClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ABC Bank Client UI")
        self.root.geometry("600x500")

        self.setup_widgets()

    def setup_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Username
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.entry_user = ttk.Entry(frame, width=30)
        self.entry_user.grid(row=0, column=1, sticky=tk.W)

        # Command Dropdown
        ttk.Label(frame, text="Command:").grid(row=1, column=0, sticky=tk.W)
        self.command_var = tk.StringVar()
        commands = [
            "create_account", "deposit", "withdraw", "transfer_to",
            "pay_loan_check", "pay_loan_transfer_to", "show_bank",
            "show_accountholders", "show_history", "show_history_filtered",
            "apply_interest"
        ]
        self.combo_command = ttk.Combobox(frame, textvariable=self.command_var, values=commands, state="readonly")
        self.combo_command.grid(row=1, column=1, sticky=tk.W)
        self.combo_command.current(0)

        # Account Number
        ttk.Label(frame, text="Account Number:").grid(row=2, column=0, sticky=tk.W)
        self.entry_acct = ttk.Entry(frame, width=30)
        self.entry_acct.grid(row=2, column=1, sticky=tk.W)

        # Amount or Filter
        ttk.Label(frame, text="Amount / Operation Type:").grid(row=3, column=0, sticky=tk.W)
        self.entry_amount = ttk.Entry(frame, width=30)
        self.entry_amount.grid(row=3, column=1, sticky=tk.W)

        # Submit Button
        self.btn_send = ttk.Button(frame, text="Send Request", command=self.send_command)
        self.btn_send.grid(row=4, column=0, columnspan=2, pady=10)

        # Response Box
        ttk.Label(frame, text="Response:").grid(row=5, column=0, sticky=tk.W)
        self.text_response = scrolledtext.ScrolledText(frame, width=70, height=15, state=tk.DISABLED)
        self.text_response.grid(row=6, column=0, columnspan=2, pady=5)

    def send_command(self):
        user = self.entry_user.get().strip()
        command = self.command_var.get().strip()
        acct_num = self.entry_acct.get().strip() or "0"
        amount = self.entry_amount.get().strip() or "0"

        # Special handling for show_history_filtered
        if command == "show_history_filtered":
            request_str = f"user={user} command={command} acct_num={acct_num} operation={amount}"
        else:
            request_str = f"user={user} command={command} acct_num={acct_num} amount={amount}"

        def thread_func():
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(ADDR)
                client_socket.send(request_str.encode())
                response = ""
                while True:
                    chunk = client_socket.recv(1024).decode()
                    if "END" in chunk:
                        response += chunk.replace("END", "")
                        break
                    response += chunk
                client_socket.close()
                self.display_response(response)
            except Exception as e:
                self.display_response(f"Error: {e}")

        threading.Thread(target=thread_func, daemon=True).start()

    def display_response(self, response):
        self.text_response.config(state=tk.NORMAL)
        self.text_response.delete("1.0", tk.END)
        self.text_response.insert(tk.END, response)
        self.text_response.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankClientGUI(root)
    root.mainloop()
