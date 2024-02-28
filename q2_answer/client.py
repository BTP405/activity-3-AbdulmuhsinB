#import libraries
import socket
import pickle

def send_task(host, port, task):
    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port)) #connect

        #send task
        s.sendall(pickle.dumps(task))

        #get result
        data = s.recv(1024)
        result = pickle.loads(data)

        return result

#tasks
tasks = [
    {'func': 'add', 'args': (0, 1)},
    {'func': 'subtract', 'args': (3, 1)},
    {'func': 'multiply', 'args': (1, 3)},
    {'func': 'divide', 'args': (8, 2)}
]

if __name__ == "__main__":
    for task in tasks:
        result = send_task('localhost', 8080, task)
        print("Result:", result)
