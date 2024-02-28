#import libraries
import socket
import pickle

#functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

# functions that will be pickled tasks
functions = {'add': add, 'subtract': subtract, 'multiply': multiply, 'divide': divide}

def worker_node(host, port):
    #creating socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))    #binding
        s.listen()  #listening

        print(f"Worker node listening on {host}:{port}")

        while True: #loop
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                #get task
                data = conn.recv(1024)
                if not data:
                    break  # No more tasks, exit loop

                task = pickle.loads(data)

                #tasks executed, and results saved into result
                func_name, args = task['func'], task['args']
                result = functions[func_name](*args)

                #sends results
                conn.sendall(pickle.dumps(result))

        # Close the socket
        s.close()

if __name__ == "__main__":
    worker_node('localhost', 8080)
