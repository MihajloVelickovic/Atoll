from src.enums.cpukonfig import CpuKonfig
from src.models.cpu import Cpu
from src.gui.gui import Gui
from src.gui.input import primeni_hover_efekat, ukloni_hover_efekat
from src.enums.boje import Boje
from src.gui.renderer import prikazi_kraj_pobeda
from src.models.igra import Igra
from src.gui.renderer import nacrtaj_tablu, prikazi_kraj_nema_slobodnih
import pygame

if __name__ == "__main__":

    Gui.setup_dpi_awareness()

    gui = Gui()

    # igra = Igra.debug_konstrukcija(5, True, True, False)
    # igra = Igra.debug_konstrukcija(5, False, False, True)
    igra = Igra.konstrukcija()
    if igra.cpu_partija:
        Cpu.postavi_vreme_trazenja(igra.tabla.n)
    gui.init_pygame()
    gui.izracunaj_dimenzije_polja(igra.tabla.n)

    # glavna petlja
    running = True

    # crtanje table pre pokretanja glavnog loopa
    gui.screen.fill(Boje.SIVA_POZADINA.value)
    gui.offset_x, gui.offset_y = nacrtaj_tablu(gui.screen, igra.tabla, gui.sirina_polja, gui.labele)
    pygame.display.flip()
    boje_u_redu = []
    selektovan_red_ili_polje = ['']
    stara_selekcija = None
    while running:

        # AI potez (pre event handling-a jer AI moze prvi da igra)
        if igra.cpu_partija and not igra.kraj_igre[0] and igra.cpu_na_potezu():
            igra.odigraj_cpu_potez(gui)
        else:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    continue

                if igra.kraj_igre[0]:
                    continue

                # ako je pritisnut escape, gasi se program
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        continue

                if event.type == pygame.KEYUP:
                    # ako je pritisnut enter, odigrava potez na selektovanom polju
                    # (ako je neko polje uopste selektovano)

                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        polje_str = ''.join(selektovan_red_ili_polje)
                        if len(polje_str) > 1:
                            polje = igra.tabla[polje_str]
                            if polje is not None:
                                idx = igra.tabla.raspored_polja.index(polje)
                                gui.obradi_unos_sa_tastature(igra, polje, idx, gui)
                                selektovan_red_ili_polje = ['']
                                stara_selekcija = None

                    # u niz polja se unose samo validni elementi
                    # cifre (0-9), slova od z do poslednjeg validnog za igra.tabla.n
                    elif ((ord('0') <= event.key <= ord('9') or
                           ord('A') <= event.key <= ord('Z') or
                           ord('a') <= event.key <= ord('z')) and
                          (ord('0') <= event.key <= ord('9') or
                           igra.tabla.n * 2 > (ord(chr(event.key).upper()) - ord('A')) % 25)):

                        # uppercase karakter koji je sada pretisnut
                        # reduntandno ako je broj ali sta da se radi
                        najnovije_dugme = chr(event.key).upper()

                        # ako je uneseno slovo, resetuje se lista koja pamti selekciju
                        # i novo slovo se postavlja za prvi element
                        # primenjuje se hover efekat svim poljima tog slova
                        if najnovije_dugme.isalpha():
                            selektovan_red_ili_polje.clear()
                            selektovan_red_ili_polje.append(najnovije_dugme)
                            gui.obradi_promenu_hovera_tastatura(igra, boje_u_redu, stara_selekcija)
                            stara_selekcija = selektovan_red_ili_polje[0]
                            boje_u_redu = [primeni_hover_efekat(x) for x in igra.tabla[selektovan_red_ili_polje[0]]]

                        # ako je unesen broj, nakon sto zasigurno vec ima slova na prvoj poziciji
                        # i s uslovom da mogu najvise 2 broja da se unesu,
                        # suzavamo selekciju na konkretno polje zadato prethodnim slovom, i novim brojem
                        # radi i za dvocifrene brojeve!!
                        if '' not in selektovan_red_ili_polje and len(
                                selektovan_red_ili_polje) < 3 and najnovije_dugme.isdigit():
                            selektovan_red_ili_polje.append(najnovije_dugme)
                            polje_str = ''.join(selektovan_red_ili_polje)
                            if igra.tabla[polje_str]:
                                gui.obradi_promenu_hovera_tastatura(igra, boje_u_redu, stara_selekcija)
                                stara_selekcija = polje_str
                                boje_u_redu = primeni_hover_efekat(igra.tabla[polje_str])

                # u ovom i sledecem eventu se , osim njihovih
                # standardnih zaduzenja, ciste hoveri i selekcije
                # unete tastaturom (prethodni event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selektovan_red_ili_polje.clear()
                    selektovan_red_ili_polje.append('')
                    gui.obradi_promenu_hovera_tastatura(igra, boje_u_redu, stara_selekcija)
                    stara_selekcija = None
                    if not igra.cpu_na_potezu():
                        gui.obradi_klik(igra, event.pos)

                elif event.type == pygame.MOUSEMOTION:
                    selektovan_red_ili_polje.clear()
                    selektovan_red_ili_polje.append('')
                    gui.obradi_promenu_hovera_tastatura(igra, boje_u_redu, stara_selekcija)
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
