import socket
import threading
import pickle
import sys

# Define server address and port
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5555

# Initialize server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()

clients = []
world_state = []

# Create initial world state
for z in range(10):
    for x in range(10):
        voxel_data = {'position': (x, 0, z), 'texture': 'grass', 'color': 'green'}
        world_state.append(voxel_data)

# Lock to manage access to the clients list
clients_lock = threading.Lock()

# Flag to signal server shutdown
shutdown_flag = threading.Event()

def broadcast(message):
    with clients_lock:
        for client in clients:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client):
    # Send initial world state to new client
    client.send(pickle.dumps({'type': 'world_state', 'data': world_state}))
    
    while not shutdown_flag.is_set():
        try:
            data = client.recv(4096)
            if not data:
                break
            # Broadcast received data to all other clients
            broadcast(data)
        except (ConnectionResetError, ConnectionAbortedError):
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove client from the list safely
    with clients_lock:
        if client in clients:
            clients.remove(client)
    client.close()

def main():
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    while not shutdown_flag.is_set():
        try:
            client, addr = server.accept()
            print(f"Connection from {addr}")
            with clients_lock:
                clients.append(client)
            threading.Thread(target=handle_client, args=(client,)).start()
        except socket.timeout:
            continue

def shutdown_server():
    shutdown_flag.set()
    # Close all client connections
    with clients_lock:
        for client in clients:
            client.close()
    server.close()
    print("Server shut down.")
    exit()

if __name__ == "__main__":
    # Run the server in a separate thread
    server_thread = threading.Thread(target=main)
    server_thread.start()
    
    # Wait for user input to shut down the server
    input("\nPress Enter to shut down the server...\n\n")
    shutdown_server()
    server_thread.join()
