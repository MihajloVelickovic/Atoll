import math

from src.models.igra import Igra
import pygame
from src.models.tabla import Tabla
from src.gui.renderer import nacrtaj_tablu
from src.gui.input import nadji_kliknuto_polje
import ctypes
import platform

if __name__ == "__main__":
    # Postavljanje dpi awareness
    if platform.system() == "Windows":
        try:
            # Windows 8.1 i noviji
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            try:
                # Windows Vista i noviji
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass

    igra = Igra.konstrukcija()
    igra.tabla.prikaz_polja()

    pygame.init()

    info = pygame.display.Info()
    screen_width = int(info.current_w * 0.9)
    screen_height = int(info.current_h * 0.80)
    screen = pygame.display.set_mode((screen_width, screen_height))

    tabla = igra.tabla
    # HEX_SIZE = 30
    # sirina polja = 2 * HEX_SIZE
    # visina polja = sqrt(3) × HEX_SIZE
    max_board_height = screen_height * 0.9
    HEX_SIZE = max_board_height / ((2 * tabla.n + 1) * math.sqrt(3))
    running = True
    offset_x, offset_y = 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                kliknuto = nadji_kliknuto_polje(event.pos, tabla, HEX_SIZE, offset_x, offset_y)
                if kliknuto:
                    print(f"Kliknuto: {kliknuto.slovo}{kliknuto.broj}")

        screen.fill((30, 30, 40))
        offset_x, offset_y = nacrtaj_tablu(screen, tabla, HEX_SIZE)
        pygame.display.flip()

    pygame.quit()