import socket
import threading
import pickle  # For serializing player data

# Define server address and port
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5555

# Initialize server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()

clients = []
world_state = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)

def handle_client(client):
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            # Broadcast received data to all other clients
            broadcast(data)
        except:
            break

    client.close()
    clients.remove(client)

def main():
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    main()
