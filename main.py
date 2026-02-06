from gui.gui import Gui
from gui.renderer import koordinate_polja
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
    # igra = Igra.debug_konstrukcija(3, False, False, True)

    gui.init_pygame()
    gui.izracunaj_dimenzije_polja(igra.tabla.n)

    #glavna petlja
    running = True

    # crtanje table pre pokretanja glavnog loopa
    gui.screen.fill(Boje.SIVA_POZADINA.value)
    gui.offset_x, gui.offset_y = nacrtaj_tablu(gui.screen, igra.tabla, gui.sirina_polja, gui.labele)
    pygame.display.flip()

    kliknuta_dugmat_sliding_window = ['', '']
    stari_string = None
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

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                        continue

                if igra.kraj_igre[0]:
                    continue

                if event.type == pygame.KEYUP:
                    if  48 <= event.key <= 57 or 65 <= event.key <= 90 or 97 <= event.key <= 122:
                        kliknuta_dugmat_sliding_window[0] = kliknuta_dugmat_sliding_window[1]
                        kliknuta_dugmat_sliding_window[1] = chr(event.key).upper()

                if ('' not in kliknuta_dugmat_sliding_window and
                       not kliknuta_dugmat_sliding_window[0].isdecimal() and
                       not kliknuta_dugmat_sliding_window[1].isalpha()):

                    polje_str = ''.join(kliknuta_dugmat_sliding_window)
                    polje = igra.tabla[polje_str]
                    if polje is not None and stari_string != polje_str:
                        stari_string = polje_str
                        idx = igra.tabla.raspored_polja.index(polje)
                        gui.obradi_unos_sa_tastature(igra, polje, idx, gui)

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