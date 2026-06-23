import socket

def connect():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    server_socket.bind((ip, 12345))

    server_socket.listen(1)
    print("Server is listening on port 12345...")

    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established")

    return server_socket, client_socket, addr

def receive_data(client_socket):
    message_in = client_socket.recv(1024).decode()
    print(f"Recieved data: {message_in}")
    return message_in

def send_data(client_socket, message_out):
    client_socket.send(message_out.encode())
    print("Response sent to the client.")

def close_connection(server_socket):
    server_socket.close()
    print("Socket closed.")
