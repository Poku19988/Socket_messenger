import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HOST = "0.0.0.0"
PORT = 8080

connected_users = {}  # {username: socket}

def broadcast_user_list():
    """Send the updated user list to all connected clients."""
    user_list = ",".join(connected_users.keys())
    message = f"/users {user_list}".encode("utf-8")
    logging.info(f"Broadcasting user list: {user_list}")  # Debugging

    for client_socket in connected_users.values():
        try:
            client_socket.sendall(message)
        except Exception as e:
            logging.error(f"Failed to send user list to a client: {e}")  # Debugging

def broadcast_message(sender_username, message):
    """Broadcast a chat message to all clients except the sender."""
    formatted_message = f"{sender_username}: {message}".encode("utf-8")
    for username, client_socket in connected_users.items():
        if username != sender_username:
            try:
                client_socket.sendall(formatted_message)
            except Exception as e:
                logging.error(f"Failed to send message to {username}: {e}")

def handle_client(client_socket, client_address):
    username = None
    try:
        client_socket.sendall("Enter your username: ".encode("utf-8"))
        username = client_socket.recv(1024).decode("utf-8").strip()

        if not username or username in connected_users:
            client_socket.sendall("Username is invalid or already taken.".encode("utf-8"))
            client_socket.close()
            return

        connected_users[username] = client_socket
        logging.info(f"{username} connected from {client_address}")

        broadcast_user_list()  # Notify all clients of the updated user list

        while True:
            message = client_socket.recv(1024).decode("utf-8").strip()
            if not message:
                break  # Client disconnected
            if message.lower() == "exit":
                break
            elif message == "/list":
                send_user_list(client_socket)  # Send only to the requester
            else:
                broadcast_message(username, message)  # Broadcast chat message to all clients

    except Exception as e:
        logging.error(f"Error with {username}: {e}")
    finally:
        if username in connected_users:
            del connected_users[username]
            logging.info(f"{username} disconnected.")
            broadcast_user_list()  # Update all clients
        client_socket.close()

def send_user_list(client_socket):
    """Sends the current user list to the requesting client."""
    user_list = ",".join(connected_users.keys())
    try:
        client_socket.sendall(f"/users {user_list}".encode("utf-8"))
    except Exception as e:
        logging.error(f"Failed to send user list: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    main()