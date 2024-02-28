#import libraries
import socket
import pickle
import threading
import sys

#function to send message
def send_message(client_socket, message):
    try:
        # Pickle/send message
        client_socket.send(pickle.dumps(message))
    except Exception as e:
        print("Error sending message:", e)


HOST = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# receive/unpickle messages
def receive_messages():
    while True:
        try:
            # receive pickled message
            data = client_socket.recv(4096)
            if not data:
                break

            # unpickle message
            message, sender_name = pickle.loads(data)

            # print message and the sender's name
            print(f"\nMessage from {sender_name}: {message}\nEnter message, click (~) to Exit: ")

        except Exception as e:
            print("Error receiving message:", e)
            break

    # Close the socket
    client_socket.close()
    sys.exit()

# thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# send name
name = input("Enter your name: ")
client_socket.send(name.encode())

#loop 
while True:
    message = input("Enter message, click (~) to Exit: ")

    # Check if the input is '~'
    if message == '~':
        # close the client
        client_socket.close()
        sys.exit()

    #send message along with name
    send_message(client_socket, (message, name))
