## 1. Description

This is a client program for an online message board system. The client can send commands to a server to POST, GET, DELETE messages, and QUIT the session. The server runs on a specified IP address and port and supports these commands.

## 2. Requirements

- Python 3.x
- A running instance of the server program provided in the project demo

## 3. Usage

To run the client program, use the following command:
python socket_client <server_ip> <server_port>

Replace `<server_ip>` and `<server_port>` with the actual IP address and port number of your server(127.0.0.1:16111).

## 4. Commands

- **POST**: Allows the client to send a message to the server. The message ends with a `#` symbol.

- **GET**: Requests all previously received messages from the server.

- **DELETE**: Deletes messages with specified IDs from the server. The IDs end with a `#` symbol.

- **QUIT**: Informs the server to close the current session.

## 5. Code Structure

- **MessageBoardClient**: The main class that handles the connection to the server and the sending/receiving of commands and responses.
  - `__init__(self, server_ip, server_port)`: Initializes the client with the server IP and port.
  - `connect_to_server(self)`: Connects to the server.
  - `send_command(self, command)`: Sends a command to the server.
  - `receive_response(self)`: Receives a response from the server.
  - `post_message(self)`: Handles the POST command.
  - `get_messages(self)`: Handles the GET command.
  - `delete_messages(self)`: Handles the DELETE command.
  - `quit(self)`: Handles the QUIT command.
  - `run(self)`: Main loop to handle user input and execute commands.


