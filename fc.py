import socket
import os

HOST = "127.0.0.1"
PORT = 12344
BUFFER_SIZE = 1024
CLIENT_DIR = "client_files"

if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print("Connected to file server. Commands: LIST, UPLOAD <file name>, DOWNLOAD <file name>, DELETE <file name>, EXIT")

    while True:
        command = input("Enter command: ").strip()
        if not command:
            continue
        command_data=command
        
        cmd = command.split()[0].upper()
        
        if cmd == "LIST":
            client.send(command_data.encode())
            data = client.recv(BUFFER_SIZE).decode()
            print("Files on server:\n", data)

        elif cmd == "UPLOAD" and len(command.split()) == 2:
            filename = command.split()[1]
            filepath = os.path.join(CLIENT_DIR, filename)

            if os.path.exists(filepath):
                client.send(command_data.encode())
                if client.recv(BUFFER_SIZE) == b"READY":
                    with open(filepath, "rb") as f:
                        while (chunk := f.read(BUFFER_SIZE)):
                            client.send(chunk)
                    client.send(b"EOF")
                print(client.recv(BUFFER_SIZE).decode())
                os.remove(filepath)
            else:
                print("File does not exist in client directory")

        elif cmd == "DOWNLOAD" and len(command.split()) == 2:
            client.send(command_data.encode())
            filename = command.split()[1]
            filepath = os.path.join(CLIENT_DIR, filename)
            data = client.recv(BUFFER_SIZE)
            if data == b"READY":
                with open(filepath, "wb") as f:
                    while True:
                        file_data = client.recv(BUFFER_SIZE)
                        if file_data == b"EOF":
                            break
                        f.write(file_data)
                print(f"Downloaded {filename} to client_files/")
            else:
                print(data.decode())

        elif cmd == "DELETE":
            client.send(command_data.encode())
            print(client.recv(BUFFER_SIZE).decode())

        elif cmd == "QUIT":
            print(client.recv(BUFFER_SIZE).decode())
            break

        else:
            print("invalid command")
            continue

    client.close()


if __name__ == "__main__":
    main()