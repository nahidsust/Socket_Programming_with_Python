import socket
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))
server.listen(1)
c, a = server.accept()
print(a)

print_lock = threading.Lock()  # Lock for printing

def receive(c):
    while True:
        
            data = c.recv(1024)
            if not data:
                break
            #with print_lock:
            print(f"from client: {data.decode()}")
            if data.decode().lower() == 'bye':
                break

def send(c):
    while True:
            msg = input("")
            c.send(msg.encode())
            if msg.lower() == 'bye':
                break
     

recv_thread = threading.Thread(target=receive, args=(c,))
send_thread = threading.Thread(target=send, args=(c,))

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()
server.close()
