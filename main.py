from gui.gui import Gui
from gui.input import primeni_hover_efekat, ukloni_hover_efekat
from src.enums.boje import Boje
from src.gui.renderer import prikazi_kraj_pobeda
from src.models.igra import Igra
from src.gui.renderer import nacrtaj_tablu, prikazi_kraj_nema_slobodnih
import pygame

if __name__ == "__main__":

    Gui.setup_dpi_awareness()

    gui = Gui()

    #igra = Igra.konstrukcija()
    igra = Igra.debug_konstrukcija(7, False, True, False)
    # igra = Igra.debug_konstrukcija(3, False, False, True)

    gui.init_pygame()
    gui.izracunaj_dimenzije_polja(igra.tabla.n)

    #glavna petlja
    running = True

    # crtanje table pre pokretanja glavnog loopa
    gui.screen.fill(Boje.SIVA_POZADINA.value)
    gui.offset_x, gui.offset_y = nacrtaj_tablu(gui.screen, igra.tabla, gui.sirina_polja, gui.labele)
    pygame.display.flip()
    kliknuta_dugmad_sliding_window = []
    boje_u_redu = []
    selected = ['']
    stara_selekcija = None
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
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        continue

                if igra.kraj_igre[0]:
                    continue

                if event.type == pygame.KEYUP:
                    # u listu se dodaju samo validna slova (slova od a
                    if event.key == pygame.K_RETURN:

                        # if not len(kliknuta_dugmad_sliding_window) < 2:
                        #     if kliknuta_dugmad_sliding_window[-2].isalpha():
                        #         kliknuta_dugmad_sliding_window = kliknuta_dugmad_sliding_window[-2:]
                        #     else:
                        #         kliknuta_dugmad_sliding_window = kliknuta_dugmad_sliding_window[-3:]
                        #
                        # if not (len(kliknuta_dugmad_sliding_window) < 2 or
                        #         len(kliknuta_dugmad_sliding_window) > 3 or
                        #         kliknuta_dugmad_sliding_window[0].isdecimal() or
                        #         kliknuta_dugmad_sliding_window[1].isalpha() or
                        #         len(kliknuta_dugmad_sliding_window) == 3 and kliknuta_dugmad_sliding_window[2].isalpha()):
                        #
                        #     polje_str = ''.join(kliknuta_dugmad_sliding_window)
                        #     if not (int(polje_str[1:]) < 0 or int(polje_str[1:]) > igra.tabla.n * 2):
                        #         polje = igra.tabla[polje_str]
                        #         if polje is not None:
                        #             idx = igra.tabla.raspored_polja.index(polje)
                        #             gui.obradi_unos_sa_tastature(igra, polje, idx, gui)
                        #     else:
                        #         print(f"Polje {polje_str} ne postoji")
                        # kliknuta_dugmad_sliding_window.clear()
                        polje_str = ''.join(selected)
                        polje = igra.tabla[polje_str]

                        if polje is not None:
                            idx = igra.tabla.raspored_polja.index(polje)
                            gui.obradi_unos_sa_tastature(igra, polje, idx, gui)


                    elif ((ord('0') <= event.key <= ord('9') or
                           ord('A') <= event.key <= ord('Z') or
                           ord('a') <= event.key <= ord('z')) and
                          (ord('0') <= event.key <= ord('9') or
                           igra.tabla.n * 2 > (ord(chr(event.key).upper()) - ord('A')) % 25)):

                        kliknuta_dugmad_sliding_window.append(chr(event.key).upper())

                        if kliknuta_dugmad_sliding_window[-1].isalpha():
                            selected.clear()
                            selected.append(kliknuta_dugmad_sliding_window[-1])
                            if boje_u_redu:
                                try:
                                    for x, b in zip(igra.tabla[stara_selekcija], boje_u_redu):
                                        ukloni_hover_efekat(x, b)
                                except TypeError:
                                    ukloni_hover_efekat(igra.tabla[stara_selekcija], boje_u_redu)
                            stara_selekcija = selected[0]
                            a = igra.tabla[selected[0]][1:-1]
                            boje_u_redu = [primeni_hover_efekat(x) for x in igra.tabla[selected[0]]]

                        if '' not in selected and len(selected) < 3 and kliknuta_dugmad_sliding_window[-1].isdigit():
                            selected.append(kliknuta_dugmad_sliding_window[-1])
                            polje_str = ''.join(selected)
                            if igra.tabla[polje_str]:
                                if boje_u_redu:
                                    try:
                                        for x, b in zip(igra.tabla[stara_selekcija], boje_u_redu):
                                            ukloni_hover_efekat(x, b)
                                    except TypeError:
                                        ukloni_hover_efekat(igra.tabla[stara_selekcija], boje_u_redu)
                                stara_selekcija = polje_str
                                boje_u_redu = primeni_hover_efekat(igra.tabla[polje_str])

                        print(selected)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected = ['']
                    if boje_u_redu:
                        try:
                            for x, b in zip(igra.tabla[stara_selekcija], boje_u_redu):
                                ukloni_hover_efekat(x, b)
                        except TypeError:
                            ukloni_hover_efekat(igra.tabla[stara_selekcija], boje_u_redu)
                    stara_selekcija = None
                    if not igra.cpu_na_potezu():
                        gui.obradi_klik(igra, event.pos)

                elif event.type == pygame.MOUSEMOTION:
                    selected = ['']
                    if boje_u_redu:
                        try:
                            for x, b in zip(igra.tabla[stara_selekcija], boje_u_redu):
                                ukloni_hover_efekat(x, b)
                        except TypeError:
                            ukloni_hover_efekat(igra.tabla[stara_selekcija], boje_u_redu)
                    stara_selekcija = None
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