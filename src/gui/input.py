from math import sqrt

from src.gui.renderer import koordinate_polja

def nadji_kliknuto_polje(pos, tabla, size, offset_x, offset_y):
    mx, my = pos

    for polje in tabla.raspored_polja:
        x, y = koordinate_polja(polje, tabla, size, offset_x, offset_y)

        size_y = sqrt(3) * size / 2
        if x - size < mx < x + size and y - size_y < my < y + size_y:
            return polje

    return None