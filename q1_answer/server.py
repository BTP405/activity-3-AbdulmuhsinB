#import livraries
import socket
import pickle

def save_file_from_client(file_data, save_path):
    try:
        with open(save_path, 'wb') as file: # Open the file
            file.write(file_data)
        print(f"File saved successfully to: {save_path}")
        return True  # return true
    except IOError as e:  #IOError handling
        print(f"Error saving file: {e}")
        return False  #return false

def main():
    host = "127.0.0.1"
    port = 8080 
    save_directory = "files_recieved/"  # Directory to put recieved file into

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket
    server_socket.bind((host, port))  # Bind socket
    server_socket.listen(1)  # listening for connections

    print("Server listening on port", port)
    
    while True: #loop
        client_socket, addr = server_socket.accept()  # Accept connection
        print("Connection established from:", addr)  
        
        try:
            file_data = client_socket.recv(4096)  # Receive data
            if not file_data:  # Check if data was recieved
                print("No data received from client.")
                continue 

            file_object = pickle.loads(file_data)  # Unpickle data
            file_name = file_object['filename']  # get the filename
            file_content = file_object['content']  # get the file content

            save_path = save_directory + file_name  # make the save pathway
            if save_file_from_client(file_content, save_path):  # Check if file was saved
                client_socket.send(f"File saved successfully to: {save_path}".encode())  # send confimation
                client_socket.close()  # Close socket
                break
            else:
                client_socket.send("Error saving file. Please try again.".encode())  #error handling
                client_socket.close()  # Close socket
                break 

        except pickle.UnpicklingError as e:  #UnpicklingError handling
            print("Error unpickling data:", e) 
            client_socket.send("Error unpickling data. Please try again.".encode())
            client_socket.close()  # Close socket
            break 
        except Exception as e:  # exceptions handling
            print("Error:", e)  
            client_socket.send("An error occurred. Please try again.".encode())  
            client_socket.close()  # Close socket
            break 
    

if __name__ == "__main__":
    main() 
