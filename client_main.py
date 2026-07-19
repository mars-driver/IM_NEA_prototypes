import gui
import client

homeserver_ip = "192.168.1.122"
schoolserver_ip = "10.56.80.136"
localhost = "127.0.0.1"

#client_socket = client.connect(server_ip)
#gui.proto_GUI_client(client_socket, server_ip)

client.run_client(homeserver_ip)