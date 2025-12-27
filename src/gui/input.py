from src.gui.renderer import koordinate_polja


def nadji_kliknuto_polje(pos, tabla, size, offset_x, offset_y):
    mx, my = pos

    for polje in tabla.raspored_polja:
        x, y = koordinate_polja(polje, tabla, size, offset_x, offset_y)
        # Proveri da li je klik unutar kruga koji opisuje heksagon
        if (mx - x) ** 2 + (my - y) ** 2 <= (size * 1.2) ** 2:
            return polje

    return None