import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import queue

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.message_queue = queue.Queue()  # For thread-safe message handling

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.root.after(100, self.process_messages)  # Process messages in the main thread
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            self.root.quit()

        self.username = None
        self.create_username_screen()

    def create_username_screen(self):
        """Create the username selection screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Username:").pack(pady=5)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=5)
        tk.Button(self.root, text="Join", command=self.send_username).pack(pady=5)

    def send_username(self):
        """Send the chosen username to the server."""
        username = self.entry_username.get().strip()
        if username:
            self.client_socket.sendall(username.encode("utf-8"))
            self.username = username
            self.create_user_selection_screen()
            self.request_user_list()  # Automatically request the user list

    def create_user_selection_screen(self):
        """Create the user selection screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Online Users:").pack(pady=5)
        
        # Frame to hold the user list buttons
        self.user_list_frame = tk.Frame(self.root, borderwidth=2, relief="solid", bg="lightgray")
        self.user_list_frame.pack(pady=5, fill="both", expand=True)

        # Refresh button
        self.refresh_users_button = tk.Button(self.root, text="Refresh Users", command=self.request_user_list)
        self.refresh_users_button.pack(pady=5)

    def request_user_list(self):
        """Request the list of online users from the server."""
        try:
            self.client_socket.sendall("/list".encode("utf-8"))  # Request user list
        except Exception as e:
            messagebox.showerror("Error", f"Connection lost: {e}")
            self.root.quit()

    def receive_messages(self):
        """Receive messages from the server and add them to the queue."""
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if message:
                    self.message_queue.put(message)
                else:
                    break  # Server disconnected
            except Exception as e:
                print(f"Error receiving message: {e}")  # Debugging
                break
        self.message_queue.put("Server disconnected.")
        self.root.quit()

    def process_messages(self):
        """Process messages from the queue in the main thread."""
        try:
            while True:
                message = self.message_queue.get_nowait()
                if message.startswith("/users "):
                    self.update_user_list(message[7:].split(","))
                else:
                    self.update_chat(message)
        except queue.Empty:
            pass
        self.root.after(100, self.process_messages)  # Continue processing

    def update_user_list(self, users):
        """Update the list of online users in the GUI."""
        for widget in self.user_list_frame.winfo_children():
            widget.destroy()

        if not users or users == [""]:
            tk.Label(self.user_list_frame, text="No users online, waiting...").pack()
        else:
            for user in users:
                if user != self.username:
                    tk.Button(
                        self.user_list_frame,
                        text=user,
                        command=lambda u=user: self.create_chat_screen(u)
                    ).pack(pady=2)  # Add some padding for better spacing

    def create_chat_screen(self, target_username):
        """Create the chat screen for a selected user."""
        self.target_username = target_username
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Chat with {target_username}").pack()

        self.chat_display = scrolledtext.ScrolledText(self.root, state="disabled", width=50, height=20)
        self.chat_display.pack(padx=10, pady=10)

        self.entry_message = tk.Entry(self.root, width=40)
        self.entry_message.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.back_button = tk.Button(self.root, text="Back to User List", command=self.create_user_selection_screen)
        self.back_button.pack(pady=5)

    def send_message(self):
        """Send a message to the selected user."""
        message = self.entry_message.get()
        if message:
            formatted_message = f"{self.username}: {message}"
            self.client_socket.sendall(formatted_message.encode("utf-8"))
            self.entry_message.delete(0, tk.END)
            self.update_chat(formatted_message)

    def update_chat(self, message):
        """Update the chat display with a new message."""
        if hasattr(self, "chat_display"):
            self.chat_display.config(state="normal")
            self.chat_display.insert(tk.END, message + "\n")
            self.chat_display.config(state="disabled")
            self.chat_display.yview(tk.END)

    def on_closing(self):
        """Handle window closing event."""
        self.client_socket.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()