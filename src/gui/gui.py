from math import sqrt

import pygame
import platform
import ctypes
from src.gui.input import nadji_kliknuto_polje, primeni_hover_efekat, ukloni_hover_efekat


class Gui:

    def __init__(self):
        self.screen: pygame.Surface = None
        self.sirina_polja: float = 0
        self.visina_polja: float = 0
        self.offset_x: float = 0
        self.offset_y: float = 0
        self.prethodno_hover_polje: object = None
        self.originalna_boja: object = None
        self.labele: bool = True

    @staticmethod
    def setup_dpi_awareness():
        # postavljanje dpi awareness za Windows
        if platform.system() == "Windows":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 8.1 +
            except:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()  # vista, 7, 8
                except:
                    pass

    def init_pygame(self):
        pygame.init()
        info = pygame.display.Info()
        screen_width = int(info.current_w * 0.7)
        screen_height = int(info.current_h * 0.80)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Atoll')

    def izracunaj_dimenzije_polja(self, n):
        max_board_height = self.screen.get_height() * 0.9
        self.sirina_polja = max_board_height / ((2 * n + 1) * sqrt(3))
        self.visina_polja = sqrt(3) * self.sirina_polja

    def obradi_unos_sa_tastature(self, igra, polje, idx, gui):
        gui.hover_logika(polje)
        _, self.originalna_boja = igra.odigraj_potez(polje, self.originalna_boja, idx)

    def obradi_klik(self, igra, event_pos):
        kliknuto, idx = nadji_kliknuto_polje(event_pos, igra.tabla, self.sirina_polja, self.visina_polja, self.offset_x,
                                             self.offset_y)
        _, self.originalna_boja = igra.odigraj_potez(kliknuto, self.originalna_boja, idx)

    def hover_logika(self, polje):
        ukloni_hover_efekat(self.prethodno_hover_polje, self.originalna_boja)
        self.originalna_boja = primeni_hover_efekat(polje)
        self.prethodno_hover_polje = polje

    def obradi_hover(self, event_pos, tabla):
        hover, idx = nadji_kliknuto_polje(event_pos, tabla, self.sirina_polja, self.visina_polja, self.offset_x,
                                          self.offset_y)

        if hover != self.prethodno_hover_polje:
            # print(f"HOVER: {hover}, ORIG.BOJA:{gui.originalna_boja}") #debug
            self.hover_logika(hover)

    @staticmethod
    def obradi_promenu_hovera_tastatura(igra, boje, selekcija):
        if boje:
            try:
                for x, b in zip(igra.tabla[selekcija], boje):
                    ukloni_hover_efekat(x, b)
            except TypeError:
                ukloni_hover_efekat(igra.tabla[selekcija], boje)
