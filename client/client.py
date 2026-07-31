import socket
import threading

# CONSTANTS
port = 13108

def connect(server_ip):
    name = input("Enter username: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    print("I am connected to the server.")
    return client, name


# OLD
def send_data(client, message_out):
    client.send(message_out.encode())
    print("Message sent to server.")

def receive_data(client):
    message_in = client.recv(1024).decode()
    print(f"Received response: {message_in}")
    return message_in

def close_connection(client):
    client.close()
    print("Client socket closed.")

# NEW
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

def run_client(server_ip):
    client, name = connect(server_ip)
    start_threads(client, name)