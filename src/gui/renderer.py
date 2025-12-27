import pygame
import math
from src.models import polje


def axial_to_pixel(q, r, size):
    """
    Konvertuje axial koordinate u pixel koordinate.
    FLAT-TOP orijentacija (ravna ivica gore/dole).
    """
    x = size * (3 / 2 * q)
    y = size * (math.sqrt(3) / 2 * q + math.sqrt(3) * r)
    return x, y


def koordinate_polja(polje, tabla, size, offset_x, offset_y):
    """
    Vraća pixel koordinate centra polja na ekranu.
    """
    q, r = tabla.koordinate_polja(polje)
    x, y = axial_to_pixel(q, r, size)
    return x + offset_x, y + offset_y


def nacrtaj_polje(screen, tabla, polje, size, offset_x, offset_y):
    """Crta jedno heksagonalno polje (FLAT-TOP orijentacija)"""
    font = pygame.font.Font(None, 18)
    q, r = tabla.koordinate_polja(polje)
    x, y = axial_to_pixel(q, r, size)
    cx = x + offset_x
    cy = y + offset_y

    # Nacrtaj heksagon - FLAT-TOP (ravna ivica gore/dole)
    points = []
    for i in range(6):
        angle = math.pi / 3 * i  # BEZ rotacije za flat-top
        px = cx + size * math.cos(angle)
        py = cy + size * math.sin(angle)
        points.append((px, py))

    # Odredi boju
    if polje.boja is None:
        color = (220, 200, 160)  # Bež boja
    else:
        color = polje.boja.value

    # Nacrtaj popunjeni heksagon
    pygame.draw.polygon(screen, color, points)

    # Nacrtaj ivicu
    pygame.draw.polygon(screen, (100, 90, 70), points, 2)

    # Dodaj tekst sa koordinatama
    if not polje.granica:
        label = f"{polje.slovo}{polje.broj}"
        text = font.render(label, True, (60, 60, 60))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)


def nacrtaj_labele(screen, tabla, size, offset_x, offset_y):
    font = pygame.font.Font(None, 18)
    for polje in tabla.raspored_polja:
        if not polje.granica:
            continue

        q, r = tabla.koordinate_polja(polje)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y

        if polje.slovo == 'Z' or polje.slovo == 'N':
            label = f"{polje.broj}"
        else:
            label = f"{polje.slovo}"

        label_offset_x, label_offset_y = 0, 0

        col = 0 if polje.slovo == 'Z' else ord(polje.slovo) - ord('A') + 1
        row = polje.broj

        if polje.slovo == 'Z':
            # Leva vertikala - pomeri levo
            label_offset_x = -size * 1.8
        elif polje.slovo == 'N':
            # Desna vertikala - pomeri desno
            label_offset_x = size * 1.8
        elif row == 0 and col >= 1 and col <= tabla.n:
            # Gornja leva dijagonala (A0, B0, C0, D0, E0, F0)
            label_offset_y = -size * 1.5
        elif row == 0 and col == tabla.n:
            # G0 - vrh gore
            label_offset_y = -size * 1.5
        elif col > tabla.n and row == col - tabla.n:
            # Gornja desna dijagonala (H0, I1, J2, K3, L4, M5)
            label_offset_y = -size * 1.5
        elif col <= tabla.n and row == tabla.n + col:
            # Donja leva dijagonala (A7, B8, C9, D10, E11, F12)
            label_offset_y = size * 1.5
        elif row == 2 * tabla.n and col == tabla.n:
            # G14 - vrh dole
            label_offset_y = size * 1.5
        elif col > tabla.n and row == 2 * tabla.n:
            # Donja desna dijagonala (H14, I14, J14, K14, L14, M14)
            label_offset_y = size * 1.5

        text = font.render(label, True, (200, 200, 200))
        text_rect = text.get_rect(center=(cx + label_offset_x, cy + label_offset_y))
        screen.blit(text, text_rect)

    g_gornje = None
    g_donje = None
    for polje in tabla.raspored_polja:
        if polje.slovo == 'G' and polje.broj == 1:
            g_gornje = polje
        if polje.slovo == 'G' and polje.broj == 13:
            g_donje = polje

    if g_gornje:
        q, r = tabla.koordinate_polja(g_gornje)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y - size * 3

        text = font.render("G", True, (200, 200, 200))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)

    if g_donje:
        q, r = tabla.koordinate_polja(g_donje)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y + size * 3

        text = font.render("G", True, (200, 200, 200))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)


def izracunaj_offset(tabla, size, screen_width, screen_height):
    # Izračunava offset za centriranje table na ekranu
    min_q = min_r = float('inf')
    max_q = max_r = float('-inf')

    for polje in tabla.raspored_polja:
        q, r = tabla.koordinate_polja(polje)
        min_q = min(min_q, q)
        max_q = max(max_q, q)
        min_r = min(min_r, r)
        max_r = max(max_r, r)

    min_x, min_y = axial_to_pixel(min_q, min_r, size)
    max_x, max_y = axial_to_pixel(max_q, max_r, size)

    # Dodaj margine
    table_width = max_x - min_x + 3 * size
    table_height = max_y - min_y + 3 * size

    offset_x = (screen_width - table_width) / 2 - min_x + 1.5 * size
    offset_y = (screen_height - table_height) / 2 - min_y + 1.5 * size

    return offset_x, offset_y


def nacrtaj_tablu(screen, tabla, size=30):
    """Crta celu tablu sa automatskim centriranjem"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    offset_x, offset_y = izracunaj_offset(tabla, size, screen_width, screen_height)

    for polje in tabla.raspored_polja:
        nacrtaj_polje(screen, tabla, polje, size, offset_x, offset_y)

    nacrtaj_labele(screen, tabla, size, offset_x, offset_y)

    return offset_x, offset_y