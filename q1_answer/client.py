#import livraries
import socket
import pickle

def pickle_file(file_path):
    try:
        with open(file_path, 'rb') as file:  # Open the file
            file_content = file.read()  # getting thhe content of the file
        filename = file_path.split('/')[-1]  # Extracting file name
        return {'filename': filename, 'content': file_content}  # return a dictionary that has the filename and content in it
    except IOError as e:  # IOError handling
        print(f"Error reading file: {e}")
        return None  # Return null

def main():
    host = "127.0.0.1"
    port = 8080

    file_path = input("Enter the path of the file to be transferred: ")  # enter file path

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ceate socket object
        client_socket.connect((host, port))  # connect

        pickled_file = pickle.dumps(pickle_file(file_path))  # pickle
        client_socket.send(pickled_file)  # Send the pickled data

        server_response = client_socket.recv(1024).decode()  # saving server respons
        print("Server Response:", server_response)  # Printing server response

    except pickle.PickleError as e:  #pickleError  handling
        print("Error pickling data:", e)
    except Exception as e:  # exception handling
        print("Error:", e)

    client_socket.close()  # Close socket

if __name__ == "__main__":
    main()
