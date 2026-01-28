from src.enums.boje import Boje
from src.gui.renderer import prikazi_kraj_pobeda
from src.models.igra import Igra
from src.gui.renderer import nacrtaj_tablu, prikazi_kraj_nema_slobodnih
from src.gui.input import nadji_kliknuto_polje, primeni_hover_efekat, ukloni_hover_efekat
from dataclasses import dataclass
from math import sqrt
import ctypes
import platform
import pygame

# cuva gui podatke o tabli
@dataclass
class GUIState:
    screen: pygame.Surface = None
    sirina_polja: float = 0
    visina_polja: float = 0
    offset_x: float = 0
    offset_y: float = 0
    prethodno_hover_polje: object = None
    originalna_boja: object = None
    labele: bool = True


def setup_dpi_awareness():
    # postavljanje dpi awareness za Windows
    if platform.system() == "Windows":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1) # 8.1 +
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware() # vista, 7, 8
            except:
                pass


def init_pygame():
    pygame.init()
    info = pygame.display.Info()
    screen_width = int(info.current_w * 0.7)
    screen_height = int(info.current_h * 0.80)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Atoll')
    return screen, screen_width, screen_height


def izracunaj_dimenzije_polja(screen_height, n):
    max_board_height = screen_height * 0.9
    sirina_polja = max_board_height / ((2 * n + 1) * sqrt(3))
    visina_polja = sqrt(3) * sirina_polja
    return sirina_polja, visina_polja


def obradi_klik(igra, event_pos, gui: GUIState):
    kliknuto, idx = nadji_kliknuto_polje(event_pos, igra.tabla, gui.sirina_polja, gui.visina_polja, gui.offset_x, gui.offset_y)
    _, gui.originalna_boja = igra.odigraj_potez(kliknuto, gui.originalna_boja, idx)


def obradi_hover(event_pos, tabla, gui: GUIState):
    hover, idx = nadji_kliknuto_polje(event_pos, tabla, gui.sirina_polja, gui.visina_polja, gui.offset_x, gui.offset_y)

    if hover != gui.prethodno_hover_polje:
        ukloni_hover_efekat(gui.prethodno_hover_polje, gui.originalna_boja)
        gui.originalna_boja = primeni_hover_efekat(hover)
        gui.prethodno_hover_polje = hover


def odigraj_ai_potez(igra, gui: GUIState):
    idx = igra.ai_najbolji_potez()
    if idx is not None:
        polje = igra.tabla.raspored_polja[idx]
        _, gui.originalna_boja = igra.odigraj_potez(polje, gui.originalna_boja, idx)


if __name__ == "__main__":
    setup_dpi_awareness()

    igra = Igra.konstrukcija()
    # igra = Igra.debug_konstrukcija(5, False, False, True)

    screen, screen_width, screen_height = init_pygame()
    sirina, visina = izracunaj_dimenzije_polja(screen_height, igra.tabla.n)

    gui = GUIState(
        screen=screen,
        sirina_polja=sirina,
        visina_polja=visina,
        prethodno_hover_polje=None,
        originalna_boja=None
    )

    #glavna petlja
    running = True
    while running:
        # AI potez (pre event handling-a jer AI moze prvi da igra)
        if igra.cpu_partija and not igra.kraj_igre[0] and igra.ai_na_potezu():
            odigraj_ai_potez(igra, gui)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if igra.kraj_igre[0]:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                obradi_klik(igra, event.pos, gui)

            elif event.type == pygame.MOUSEMOTION:
                obradi_hover(event.pos, igra.tabla, gui)

        gui.screen.fill(Boje.SIVA_POZADINA.value)
        gui.offset_x, gui.offset_y = nacrtaj_tablu(gui.screen, igra.tabla, gui.sirina_polja, gui.labele)

        if igra.kraj_igre[0]:
            if igra.kraj_igre[1]:
                prikazi_kraj_pobeda(gui.screen, gui.originalna_boja)
            else:
                prikazi_kraj_nema_slobodnih(gui.screen)
        pygame.display.flip()

    pygame.quit()
    igra.sacuvaj_izvestaj(igra.kraj_igre)