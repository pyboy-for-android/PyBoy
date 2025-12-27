import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 9999

clients = []
clients_lock = threading.Lock()

def handle_client(conn, idx):
    try:
        while True:
            data = conn.recv(1)
            if not data:
                break
            # DEBUG: Imprime qué cliente envía qué byte
            print(f"C{idx} -> {data.hex()}")
            # Enviar al "otro" cliente
            other_idx = 1 - idx
            with clients_lock:
                if len(clients) > other_idx:
                    try:
                        clients[other_idx].sendall(data)
                    except:
                        break # El otro cliente se desconectó
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f"Cliente {idx} desconectado")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Importante: Nodelay también aquí
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        print("Link server listening on", PORT)

        while len(clients) < 2:
            conn, addr = s.accept()
            # Asegurar nodelay en la conexión aceptada
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            with clients_lock:
                clients.append(conn)
            print(f"Client {len(clients)-1} connected:", addr)

        # Iniciar hilos solo cuando AMBOS estén conectados para evitar pérdida de paquetes iniciales
        print("Ambos clientes conectados. Iniciando puente...")
        for i, conn in enumerate(clients):
            t = threading.Thread(target=handle_client, args=(conn, i), daemon=True)
            t.start()

        print("Link session active")
        # Mantener vivo el servidor
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()