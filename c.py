import socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',12345))
while True:
    x=input("send message to server: ")
    client.send(x.encode())
    data=client.recv(1024)
    print(f"server message: {data.decode()}")
    if data.decode()=="bye":
        break
client.close()