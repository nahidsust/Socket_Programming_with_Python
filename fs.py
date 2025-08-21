import socket
import threading
import os

# Server configuration
HOST = "127.0.0.1"
PORT = 12344
BUFFER_SIZE = 1024
SERVER_DIR = "server_files"

# Ensure the server directory exists
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
  
    while True:
            data = conn.recv(BUFFER_SIZE).decode()
            if not data:
                break

            command = data.split()
            if not command:
                continue

            cmd = command[0].upper()

            if cmd == "LIST":
                files = os.listdir(SERVER_DIR)
                conn.send("\n".join(files).encode() if files else b"No files on server")

            elif cmd == "UPLOAD" and len(command) == 2:
                filename = command[1]
                filepath = os.path.join(SERVER_DIR, filename)
                conn.send(b"READY")
                with open(filepath, "wb") as f:
                    while True:
                        file_data = conn.recv(BUFFER_SIZE)
                        if file_data == b"EOF":
                            break
                        f.write(file_data)
                conn.send(b"UPLOAD SUCCESS")

            elif cmd == "DOWNLOAD" and len(command) == 2:
                filename = command[1]
                filepath = os.path.join(SERVER_DIR, filename)
                if os.path.exists(filepath):
                    conn.send(b"READY")
                    with open(filepath, "rb") as f:
                        while (chunk := f.read(BUFFER_SIZE)):
                            conn.send(chunk)
                    conn.send(b"EOF")
                else:
                    conn.send(b"ERROR: File not found")

            elif cmd == "DELETE" and len(command) == 2:
                filename = command[1]
                filepath = os.path.join(SERVER_DIR, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    conn.send(b"DELETE SUCCESS")
                else:
                    conn.send(b"ERROR: File not found")

            elif cmd == "EXIT":
                conn.send(b"Goodbye!")
                break

            else:
                conn.send(b"Invalid command")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f" Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        handle_client(conn,addr)
       
if __name__ == "__main__":
     main()