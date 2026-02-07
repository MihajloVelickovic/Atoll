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
    najnovije_dugme = []
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
                    # ako je pritisnut enter, odigrava potez na selektovanom polju
                    # (ako je neko polje uopste selektovano)
                    if event.key == pygame.K_RETURN:

                        polje_str = ''.join(selected)
                        if len(polje_str) > 1:
                            polje = igra.tabla[polje_str]

                            if polje is not None:
                                idx = igra.tabla.raspored_polja.index(polje)
                                gui.obradi_unos_sa_tastature(igra, polje, idx, gui)
                                selected = ['']
                                stara_selekcija = None

                    # u niz polja se unose samo validni elementi
                    # cifre (0-9), slova od z do poslednjeg validnog za igra.tabla.n
                    elif ((ord('0') <= event.key <= ord('9') or
                           ord('A') <= event.key <= ord('Z') or
                           ord('a') <= event.key <= ord('z')) and
                          (ord('0') <= event.key <= ord('9') or
                           igra.tabla.n * 2 > (ord(chr(event.key).upper()) - ord('A')) % 25)):

                        najnovije_dugme= chr(event.key).upper()

                        if najnovije_dugme.isalpha():
                            selected.clear()
                            selected.append(najnovije_dugme)
                            if boje_u_redu:
                                try:
                                    for x, b in zip(igra.tabla[stara_selekcija], boje_u_redu):
                                        ukloni_hover_efekat(x, b)
                                except TypeError:
                                    ukloni_hover_efekat(igra.tabla[stara_selekcija], boje_u_redu)
                            stara_selekcija = selected[0]
                            a = igra.tabla[selected[0]][1:-1]
                            boje_u_redu = [primeni_hover_efekat(x) for x in igra.tabla[selected[0]]]

                        if '' not in selected and len(selected) < 3 and najnovije_dugme.isdigit():
                            selected.append(najnovije_dugme)
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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected.clear()
                    selected.append('')
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
                    selected.clear()
                    selected.append('')
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

# def obradi_promenu_hovera_tastatura(igra, boje, selekcija):
#     if boje:
#         try:
#             for x, b in zip(igra.tabla[selekcija], boje):
#                 ukloni_hover_efekat(x, b)
#         except TypeError:
#             ukloni_hover_efekat(igra.tabla[selekcija], boje)