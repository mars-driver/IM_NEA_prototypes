import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("10.56.80.136", 12345))
print("Connected to the server.")

client_socket.send("Hello from the client!".encode())

response = client_socket.recv(1024).decode()
print(f"Recieved response: {response}")

client_socket.close()
print("Client socket closed.")