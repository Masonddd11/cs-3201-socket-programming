import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f'Connected by {addr}')
    clients.append(conn)
    
    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            broadcast(message, conn)
        except:
            break

    conn.close()
    clients.remove(conn)
    print(f'Disconnected by {addr}')

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            client.send(message)

def simple_server():
    host = '127.0.0.1'
    port = 4300

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    simple_server()
