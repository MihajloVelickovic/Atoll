from models.igra import Igra
import pygame
from src.models.tabla import Tabla
from src.gui.renderer import nacrtaj_tablu
from src.gui.input import nadji_kliknuto_polje

if __name__ == "__main__":

    igra = Igra.konstrukcija()
    igra.tabla.prikaz_polja()

    pygame.init()
    screen = pygame.display.set_mode((1400, 900))
    pygame.display.set_caption("Atoll")

    tabla = Tabla(n=7)
    HEX_SIZE = 30

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