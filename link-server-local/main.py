from link_client import LinkClient
from pyboy import PyBoy

ROM_PATH = "/home/sergio/Downloads/PokemonCrystal.gbc"

LINK_HOST = "127.0.0.1"
LINK_PORT = 9999

link_client = LinkClient(LINK_HOST, LINK_PORT)

pyboy = PyBoy(
    ROM_PATH,
    window="SDL2",
    sound_emulated=True,
    sound_volume=100,
    link_send=link_client.send_byte,
    link_recv_queue=link_client.recv_queue,
)

try:
    while pyboy.tick():
        pass
except KeyboardInterrupt:
    print("\nCerrando por teclado...")
finally:
    # Código de limpieza para cerrar sockets y liberar recursos
    print("Cerrando conexión y emulador...")
    link_client.close()
    pyboy.stop()
