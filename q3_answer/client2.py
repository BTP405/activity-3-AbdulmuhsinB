import socket
import pickle
import threading
import sys

# Function to send message to server
def send_message(client_socket, message):
    try:
        # Pickle and send the message to server
        client_socket.send(pickle.dumps(message))
    except Exception as e:
        print("Error sending message:", e)

# Client configuration
HOST = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to receive and unpickle messages from server
def receive_messages():
    while True:
        try:
            # Receive pickled message from server
            data = client_socket.recv(4096)
            if not data:
                break

            # Unpickle the received data
            message, sender_name = pickle.loads(data)

            # Print the message with the sender's name
            print(f"\nMessage from {sender_name}: {message}\nEnter message, click (~) to Exit: ")

        except Exception as e:
            print("Error receiving message:", e)
            break

    # Close the client socket when the loop exits
    client_socket.close()
    sys.exit()

# Start a thread to receive messages from server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Send the client's chosen name to the server
name = input("Enter your name: ")
client_socket.send(name.encode())

# Main loop to send messages to server
while True:
    message = input("Enter message, click (~) to Exit: ")

    # Check if the input is '~' to exit
    if message == '~':
        # Close the client socket
        client_socket.close()
        sys.exit()

    # Send message along with sender's address (or name)
    send_message(client_socket, (message, name))
