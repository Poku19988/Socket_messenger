# Chat Application

## Description
This project is a multi-threaded chat server and client application. The server can handle multiple clients, each of whom can broadcast messages to all other clients. The client application connects to the server, sends and receives messages, and displays the list of connected users.

## Algorithms and Steps

### Server-Side Algorithm
1. **Configure Logging**
    - Set up logging to capture and format log messages.
2. **Initialize Server**
    - Define `HOST` and `PORT`.
    - Create a dictionary `connected_users` to track connected clients.
3. **Broadcast User List**
    - Compile a list of connected usernames and send it to all clients.
4. **Broadcast Message**
    - Send a chat message to all clients except the sender.
5. **Handle Client**
    - Prompt the client for a username.
    - Add the client to `connected_users`.
    - Broadcast the updated user list.
    - Continuously receive messages from the client.
    - Broadcast messages to all clients or handle special commands like `/list`.
    - Remove the client from `connected_users` when they disconnect.
6. **Send User List**
    - Send the current user list to a specific client.
7. **Main Function**
    - Initialize the server socket.
    - Bind the socket to the host and port.
    - Accept incoming connections and start a new thread for each client.

### Client-Side Algorithm
1. **Initialize Client**
    - Set up a socket connection to the server.
    - Start a thread to receive messages from the server.
    - Create a GUI for user interaction.
2. **Create Username Screen**
    - Prompt the user to enter a username.
    - Send the username to the server.
3. **Request User List**
    - Request the list of online users from the server.
4. **Receive Messages**
    - Continuously receive messages from the server and add them to a queue.
5. **Process Messages**
    - Process messages from the queue and update the GUI accordingly.
6. **Send Message**
    - Send a chat message to the server.
    - Update the chat display with the new message.
7. **Create Chat Screen**
    - Create a chat interface for interacting with a specific user.

## Threading
Threading is used to handle multiple clients simultaneously in the server and to receive messages in the client without blocking the main GUI thread. Each client connection in the server is handled in a separate thread, ensuring that one client's actions don't block others.

## Socket Binding and Accepting Connections
- **Bind**: The `bind` function assigns the specified IP address and port number to the server socket, allowing it to listen for incoming connections.
    ```python
    server_socket.bind((HOST, PORT))
    ```
- **Accept**: The `accept` function waits for incoming client connections and returns a new socket object representing the client connection and the address of the client.
    ```python
    client_socket, client_address = server_socket.accept()
    ```

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/username/repository-name.git
    ```
2. Navigate to the project directory:
    ```sh
    cd repository-name
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Start the server:
    ```sh
    python server.py
    ```
2. Start the client:
    ```sh
    python client.py
    ```

## Contributing
Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- Inspired by various online resources and tutorials.
- Special thanks to all contributors and the open-source community.
