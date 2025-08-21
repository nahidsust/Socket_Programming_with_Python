import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name (or use 'localhost' or your IP)
host = 'localhost'
port = 12345

# Bind the socket to the port
server_socket.bind((host, port))#server listen only send this address ,if use 0.0.0.0 then server listen all address 

# Listen for incoming connections (max 1 queued connection)
server_socket.listen(1)
print(f"Server listening on {host}:{port}...")

# Accept a connection
conn, addr = server_socket.accept()
print(f"Connected by or client ip and port {addr}")

# Receive data (max 1024 bytes)
data = conn.recv(1024)
print(f"Received from client: {data.decode()}")
x=data.decode()
x=x.upper()
# Send a reply back to client
conn.send(x.encode())

# Close connection
conn.close()
