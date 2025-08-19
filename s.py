import socket
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('0.0.0.0',12345))
server.listen(1)
c,a=server.accept()
print(a)
while True:
    data=c.recv(1024)
    print(f"client message:{data.decode()}")
    if data.decode()=="bye":
        break
    x=input("send message to client: ")
    c.send(x.encode())
c.close()
server.close()