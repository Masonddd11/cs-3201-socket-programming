import socket
import sys

BUFFER_SIZE = 4096

class MessageBoardClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.sock.connect((self.server_ip, self.server_port))
            print(f"Connected to server {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)

    def send_command(self, command):
        self.sock.sendall(bytes(command + '\n', 'utf-8'))

    def receive_response(self):
        response = self.sock.recv(BUFFER_SIZE).decode('utf-8')
        return response

    def post_message(self):
        print("Enter your message. End with '#' on a new line.")
        self.send_command("POST")
        while True:
            line = input()
            self.send_command(line)
            if line == "#":
                break
        response = self.receive_response()
        print(response)

    def get_messages(self):
        self.send_command("GET")
        while True:
            response = self.receive_response()
            if response == '#':
                break
            print(response)

    def delete_messages(self):
        print("Enter message IDs to delete. End with '#' on a new line.")
        self.send_command("DELETE")
        while True:
            line = input()
            self.send_command(line)
            if line == "#":
                break
        response = self.receive_response()
        print(response)

    def quit(self):
        self.send_command("QUIT")
        response = self.receive_response()
        print(response)
        self.sock.close()

    def run(self):
        while True:
            command = input("Enter command (POST, GET, DELETE, QUIT): ").strip().upper()
            if command == "POST":
                self.post_message()
            elif command == "GET":
                self.get_messages()
            elif command == "DELETE":
                self.delete_messages()
            elif command == "QUIT":
                self.quit()
                break
            else:
                self.send_command(command)
                response = self.receive_response()
                print(response)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python MessageBoardClient.py <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    client = MessageBoardClient(server_ip, server_port)
    client.run()