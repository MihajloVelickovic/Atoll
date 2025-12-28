from enums.boje import Boje
from src.models.igra import Igra
from src.gui.renderer import nacrtaj_tablu
from src.gui.input import nadji_kliknuto_polje
from math import sqrt
import ctypes
import platform
import pygame

if __name__ == "__main__":
    # postavljanje dpi awareness
    if platform.system() == "Windows":
        try:
            # 8.1 +
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            try:
                # vista, 7, 8
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass

    igra = Igra.konstrukcija()
    igra.tabla.prikaz_polja()

    pygame.init()

    info = pygame.display.Info()
    screen_width = int(info.current_w * 0.7)
    screen_height = int(info.current_h * 0.80)
    screen = pygame.display.set_mode((screen_width, screen_height))

    tabla = igra.tabla
    max_board_height = screen_height * 0.9
    sirina_polja = max_board_height / ((2 * tabla.n + 1) * sqrt(3))
    visina_polja = sqrt(3) * sirina_polja
    running = True
    offset_x, offset_y = 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                kliknuto = nadji_kliknuto_polje(event.pos, tabla, sirina_polja, visina_polja, offset_x, offset_y)
                if kliknuto:
                    print(f"Kliknuto: {kliknuto.slovo}{kliknuto.broj}")

        screen.fill(Boje.SIVA_POZADINA.value)
        offset_x, offset_y = nacrtaj_tablu(screen, tabla, sirina_polja)
        pygame.display.flip()

    pygame.quit()
