import gui
import client

server_ip = "192.168.1.122"

#client_socket = client.connect(server_ip)
#gui.proto_GUI_client(client_socket, server_ip)

client.run_client(server_ip)