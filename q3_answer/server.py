#import libraries
import socket
import threading
import pickle

# dctionary to store names
client_names = {}

# handle client connections
def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")

    while True:
        try:
            # Receive pickled message
            data = client_socket.recv(4096)
            if not data:
                break

            # Unpickle message
            message, sender_name = pickle.loads(data)

            # Print message with name
            print(f"{sender_name}: {message}")

            # send mesage to all clients but the sender
            broadcast(message, sender_name, client_socket)

        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break

    print(f"Connection from {address} closed.")
    del client_names[address]  # Remove client's name
    client_sockets.remove(client_socket)
    client_socket.close()

#send message to all clients
def broadcast(message, sender_name, sender_socket):
    for client_socket in client_sockets:
        if client_socket != sender_socket:
            try:
                #pickle and send the message 
                client_socket.send(pickle.dumps((message, sender_name)))
            except:
                client_sockets.remove(client_socket)


HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Server listening on port", PORT)

# List to store clients
client_sockets = []

# accpet incoming connections, starting new threads for each client
def accept_connections():
    while True:
        client_socket, address = server_socket.accept()
        client_sockets.append(client_socket)
        
        # recieve clients name
        name_data = client_socket.recv(1024)
        client_names[address] = name_data.decode()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# accept connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
