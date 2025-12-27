import socket
import threading

HOST = "127.0.0.1"
PORT = 9999

clients = []

def handle_client(conn, idx):
    other = 1 - idx
    try:
        while True:
            data = conn.recv(1)
            if not data:
                break
            if len(clients) > other:
                clients[other].sendall(data)
    except ConnectionResetError:
        pass
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        print("Link server listening on", PORT)

        while len(clients) < 2:
            conn, addr = s.accept()
            print("Client connected:", addr)
            clients.append(conn)

        for i, conn in enumerate(clients):
            t = threading.Thread(target=handle_client, args=(conn, i), daemon=True)
            t.start()

        print("Link session active")
        threading.Event().wait()

if __name__ == "__main__":
    main()
