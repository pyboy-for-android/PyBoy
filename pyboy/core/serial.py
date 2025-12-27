import queue

import pyboy
from pyboy.utils import MAX_CYCLES

logger = pyboy.logging.get_logger(__name__)

SERIAL_FREQ = 8192 # Hz
CPU_FREQ = 4194304 # Hz


class Serial:
    def __init__(self, mb, link_send=None, link_recv_queue=None):
        self.mb = mb
        self.SC = 0
        self.SB = 0

        self.link_send = link_send
        self.recv_queue = link_recv_queue

        self.trans_bits = 0          # usado como "ya envié"
        self.cycles_count = 0
        self.cycles_target = CPU_FREQ // SERIAL_FREQ
        self._cycles_to_interrupt = MAX_CYCLES

    def set_SB(self, value):
        self.SB = value & 0xFF

    def set_SC(self, value):
        self.SC = value & 0xFF
        if self.SC & 0x80:
            # nueva transferencia → permitir envío
            self.trans_bits = 0

    def tick(self, cycles):
        if not self.link_send or not self.recv_queue:
            self.SB = 0xFF
            return False

        if not (self.SC & 0x80):
            return False

        self.cycles_count += cycles
        if self.cycles_count < self.cycles_target:
            return False

        self.cycles_count = 0

        if self.trans_bits == 0:
            try:
                self.link_send(self.SB)
            except Exception:
                pass
            self.trans_bits = 1

        try:
            incoming = self.recv_queue.get_nowait()
        except queue.Empty:
            incoming = 0xFF  # NUNCA bloquear


        self.SB = incoming & 0xFF
        self.trans_bits = 0
        self.SC &= 0x7F  # clear transfer flag
        return True
