import socket
import threading
import queue

class LinkClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ESTA ES LA CLAVE: Desactiva el algoritmo de Nagle para enviar bytes instantáneamente
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((host, port))
        self.recv_queue = queue.Queue()
        self.running = True

        t = threading.Thread(target=self._recv_loop, daemon=True)
        t.start()

    def _recv_loop(self):
        while self.running:
            try:
                # Recibimos 1 byte exacto
                data = self.sock.recv(1)
                if data:
                    self.recv_queue.put(data[0])
                else:
                    # Si recibimos vacío, el servidor cerró. Salimos.
                    self.close()
                    break
            except Exception:
                break

    def send_byte(self, b: int):
        if not self.running:
            return
        try:
            self.sock.sendall(bytes([b & 0xFF]))
        except:
            self.close()

    def close(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass