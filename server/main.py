import gui
import server

# CONSTANTS
homehost = "192.168.1.122"
schoolhost = "10.56.80.136"
localhost = "127.0.0.1"
my_port = 12345

#gui.proto_GUI_server(my_port)
server.run_server(my_port)