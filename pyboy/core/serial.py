import queue
from pyboy.utils import MAX_CYCLES

# Asegúrate de que este archivo reemplace al original en tu instalación de PyBoy
# o que estés inyectándolo correctamente.

class Serial:
    def __init__(self, mb, link_send=None, link_recv_queue=None):
        self.mb = mb
        self.SC = 0
        self.SB = 0

        self.link_send = link_send
        self.recv_queue = link_recv_queue

        self.sent = False
        self.stopped = False
        self._cycles_to_interrupt = MAX_CYCLES

    def set_SB(self, value):
        self.SB = value & 0xFF

    def set_SC(self, value):
        self.SC = value & 0xFF
        # Si el juego inicia una transferencia (bit 7), reseteamos el estado de envío
        if self.SC & 0x80:
            self.sent = False

    def tick(self, cycles):
        if self.stopped or not self.link_send or not self.recv_queue:
            return False

        if not (self.SC & 0x80):
            return False

        # 1. Enviar byte
        if not self.sent:
            try:
                self.link_send(self.SB)
                self.sent = True
            except:
                return False

        # 2. Recibir byte (BLOQUEANTE)
        try:
            # Esperamos hasta 500ms. Si no llega nada, devolvemos False para reintentar.
            # Al ser bloqueante, el emulador se "congela" un instante esperando al otro.
            incoming = self.recv_queue.get(block=True, timeout=0.5)
            self.SB = incoming & 0xFF
            self.sent = False
            self.SC &= 0x7F 
            return True
        except queue.Empty:
            # Si hay timeout, devolvemos False. Esto evita que el emulador 
            # asuma que recibió un 0xFF por error.
            return False

    def stop(self):
        self.stopped = True