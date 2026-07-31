import socket
import threading

def connect(server_ip, port):
    name = input("Enter username: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    print("Connected to the server.")
    return client, name

def receive(client, name):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NAME":
                client.send(name.encode())
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write(client, name):
    while True:
        message = f"{name}: {input()}"
        client.send(message.encode())

def start_threads(client, name):
    receive_thread = threading.Thread(target=receive, args=(client, name))
    receive_thread.start()

    write_thread = threading.Thread(target=write, args=(client,name))
    write_thread.start()

def run_client(server_ip, port):
    client, name = connect(server_ip, port)
    start_threads(client, name)