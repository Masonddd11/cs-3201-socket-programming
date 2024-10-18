import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

class ChatClient:
    def __init__(self, host, port):
        self.username = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        self.window = tk.Tk()
        self.window.title("Chat Client")
        
        self.text_area = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10)
        
        self.entry = tk.Entry(self.window, width=50)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)
        
        self.ask_username()
        
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def ask_username(self):
        self.username = simpledialog.askstring("Username", "Enter your username:")
        if self.username:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"{self.username} has joined the chat.\n")
            self.text_area.config(state='disabled')
            self.sock.sendall(f"{self.username} has joined the chat.".encode())

    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.text_area.config(state='normal')
                    self.text_area.insert(tk.END, message + "\n")
                    self.text_area.config(state='disabled')
                    self.text_area.yview(tk.END)
            except:
                break

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"You: {message}\n")
            self.text_area.config(state='disabled')
            self.sock.sendall(f"{self.username}: {message}".encode())
            self.entry.delete(0, tk.END)

    def on_closing(self):
        self.sock.close()
        self.window.destroy()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 4300
    client = ChatClient(host, port)
    tk.mainloop()
