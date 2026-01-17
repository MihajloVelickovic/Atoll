from src.enums.boje import Boje
from src.gui.renderer import prikazi_kraj_pobeda
from src.models.igra import Igra
from src.gui.renderer import nacrtaj_tablu, prikazi_kraj_nema_slobodnih
from src.gui.input import nadji_kliknuto_polje, primeni_hover_efekat, ukloni_hover_efekat
from math import sqrt
import ctypes
import platform
import pygame

if __name__ == "__main__":
    # postavljanje dpi awareness za Windows
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

    #igra = Igra.konstrukcija()
    igra = Igra.debug_konstrukcija(5, False, False, True)
    #igra.tabla.prikaz_polja()

    pygame.init()

    info = pygame.display.Info()
    screen_width = int(info.current_w * 0.7)
    screen_height = int(info.current_h * 0.80)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Atoll')

    tabla = igra.tabla
    max_board_height = screen_height * 0.9
    sirina_polja = max_board_height / ((2 * tabla.n + 1) * sqrt(3))
    visina_polja = sqrt(3) * sirina_polja
    running = True
    offset_x, offset_y = 0, 0
    prethodno_hover_polje = None
    originalna_boja = None
    labele = True
    listen = True


    while running:
        for event in pygame.event.get():

            if event.type != pygame.QUIT and not listen:
                continue

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not igra.kraj_igre[0]:
                    kliknuto, idx = nadji_kliknuto_polje(event.pos, tabla, sirina_polja, visina_polja, offset_x, offset_y)
                    uspesno_odigrano, originalna_boja = igra.odigraj_potez(kliknuto, originalna_boja, idx)
                    if not uspesno_odigrano:
                        continue

            if event.type == pygame.MOUSEMOTION:
                hover, idx = nadji_kliknuto_polje(event.pos, tabla, sirina_polja, visina_polja, offset_x, offset_y)

                # ako se promenilo polje
                if hover != prethodno_hover_polje:
                    # vrati boju prethodnom
                    ukloni_hover_efekat(prethodno_hover_polje, originalna_boja)
                    # primeni hover na novo
                    originalna_boja = primeni_hover_efekat(hover)
                    prethodno_hover_polje = hover

        screen.fill(Boje.SIVA_POZADINA.value)
        offset_x, offset_y = nacrtaj_tablu(screen, tabla, sirina_polja, labele)

        if igra.kraj_igre[0]:
            listen = False
            if igra.kraj_igre[1]:
                prikazi_kraj_pobeda(screen, originalna_boja)
            else:
                prikazi_kraj_nema_slobodnih(screen)
        pygame.display.flip()

    pygame.quit()

    igra.sacuvaj_izvestaj(igra.kraj_igre)
