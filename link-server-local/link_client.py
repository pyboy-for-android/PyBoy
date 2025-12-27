import socket
import threading
import queue

class LinkClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.recv_queue = queue.Queue()
        self.running = True

        t = threading.Thread(target=self._recv_loop, daemon=True)
        t.start()

    def _recv_loop(self):
        while self.running:
            try:
                data = self.sock.recv(1)
                if data:
                    self.recv_queue.put(data[0])
            except:
                break

    def send_byte(self, b: int):
        try:
            self.sock.sendall(bytes([b & 0xFF]))
        except:
            pass

    def close(self):
        self.running = False
        self.sock.close()
