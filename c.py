import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

print_lock = threading.Lock()  # lock for printing

def receive(c):
    while True:
            data = c.recv(1024)
            if not data:
                break
            with print_lock:
                print(f"from server: {data.decode()}")

def send(c):
    while True:
            msg = input("")
            c.send(msg.encode())
            if msg.lower() == 'bye':
                break

recv_thread = threading.Thread(target=receive, args=(client,))
send_thread = threading.Thread(target=send, args=(client,))

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()

client.close()
