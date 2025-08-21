import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server on localhost and port 12345
server_ip="localhost" # if server is same machine use:localhost,if in same LAN or wifi use:private ip ,if anywhere in the world use : public ip(router assign devices private ip and isp assign device puplic ip)

client_socket.connect((server_ip, 12345))

# Send some data
message=input("Enter a message: ")
client_socket.send(message.encode())

# Receive response from the server
response = client_socket.recv(1024)
print(f"Received from server: {response.decode()}")

# Close the connection
client_socket.close() 