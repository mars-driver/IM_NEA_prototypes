import socket

def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(("10.56.80.136", 12345))
    print("Connected to the server.")

def send_data(client_socket, message_out):
    client_socket.send(message_out.encode())
    print("Message sent to server.")

def receive_data(client_socket):
    message_in = client_socket.recv(1024).decode()
    print(f"Recieved response: {message_in}")

def close_connection(client_socket):
    client_socket.close()
    print("Client socket closed.")

connect()