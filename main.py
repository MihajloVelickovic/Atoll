from gui.gui import Gui
from src.enums.boje import Boje
from src.gui.renderer import prikazi_kraj_pobeda
from src.models.igra import Igra
from src.gui.renderer import nacrtaj_tablu, prikazi_kraj_nema_slobodnih
import pygame

if __name__ == "__main__":

    Gui.setup_dpi_awareness()

    gui = Gui()

    #igra = Igra.konstrukcija()
    igra = Igra.debug_konstrukcija(3, True, True, True)

    gui.init_pygame()
    gui.izracunaj_dimenzije_polja(igra.tabla.n)

    #glavna petlja
    running = True

    # crtanje table pre pokretanja glavnog loopa
    gui.screen.fill(Boje.SIVA_POZADINA.value)
    gui.offset_x, gui.offset_y = nacrtaj_tablu(gui.screen, igra.tabla, gui.sirina_polja, gui.labele)
    pygame.display.flip()

    while running:

        # AI potez (pre event handling-a jer AI moze prvi da igra)
        if igra.cpu_partija and not igra.kraj_igre[0] and igra.cpu_na_potezu():
            igra.odigraj_cpu_potez(gui)
            #time.sleep(0.5)
            #continue
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue

                if igra.kraj_igre[0]:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not igra.cpu_na_potezu():
                        gui.obradi_klik(igra, event.pos)

                elif event.type == pygame.MOUSEMOTION:
                    gui.obradi_hover(event.pos, igra.tabla)

        gui.offset_x, gui.offset_y = nacrtaj_tablu(gui.screen, igra.tabla, gui.sirina_polja, gui.labele)

        if igra.kraj_igre[0]:
            if igra.kraj_igre[1]:
                prikazi_kraj_pobeda(gui.screen, gui.originalna_boja)
            else:
                prikazi_kraj_nema_slobodnih(gui.screen)
        pygame.display.flip()

    pygame.quit()
    igra.sacuvaj_izvestaj(igra.kraj_igre)