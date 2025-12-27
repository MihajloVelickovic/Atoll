import pygame
import math



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

    # Dodaj tekst SAMO za negranična polja
    if not polje.granica:
        font = pygame.font.Font(None, 18)
        label = f"{polje.slovo}{polje.broj}"
        text = font.render(label, True, (60, 60, 60))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)


def nacrtaj_labele(screen, tabla, size, offset_x, offset_y):
    """Crta labele (slova i brojeve) van graničnih polja"""
    font = pygame.font.Font(None, 22)

    n = tabla.n

    # Dinamički odredi middle slovo (G za n=7, E za n=5, C za n=3)
    # Z je kolona 0, A je kolona 1, pa middle je kolona n
    middle_slovo = chr(ord('Z') + n) if n == 0 else chr(ord('A') + n - 1)

    # Prvo nacrtaj labele za granična polja
    for polje in tabla.raspored_polja:
        if not polje.granica:
            continue

        q, r = tabla.koordinate_polja(polje)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y

        # Odredi labelu i offset
        label_offset_x, label_offset_y = 0, 0

        col = 0 if polje.slovo == 'Z' else ord(polje.slovo) - ord('A') + 1
        row = polje.broj

        # LEVA VERTIKALA (Z kolona) - brojevi levo
        if polje.slovo == 'Z':
            label = f"{polje.broj}"
            label_offset_x = -size * 1.5
            label_offset_y = size * 0.8

        # DESNA VERTIKALA (N kolona) - brojevi desno
        elif col == 2 * n:  # Dinamički - poslednja kolona
            label = f"{polje.broj}"
            label_offset_x = size * 1.5
            label_offset_y = -size * 0.8

        # GORNJA LEVA DIJAGONALA (A do middle-1 sa row=0)
        elif row == 0 and 1 <= col < n:
            label = f"{polje.slovo}"
            #label_offset_x = -size * 1.3
            label_offset_y = -size * 1.5

        # GORNJI VRH (middle slovo sa row=0)
        elif row == 0 and col == n:
            label = f"{polje.slovo}"
            label_offset_y = -size * 1.5

        # GORNJA DESNA DIJAGONALA (middle+1 do pred-poslednje kolone gde je row=col-n)
        elif col > n and col < 2 * n and row == col - n:
            label = f"{polje.slovo}"
            #label_offset_x = size * 1.3
            label_offset_y = -size * 1.5

        # DONJA LEVA DIJAGONALA (A do middle-1 gde je row=n+col)
        elif 1 <= col < n and row == n + col:
            label = f"{polje.slovo}"
            #label_offset_x = -size * 1.3
            label_offset_y = size * 1.5

        # DONJI VRH (middle slovo sa row=2*n)
        elif col == n and row == 2 * n:
            label = f"{polje.slovo}"
            label_offset_y = size * 1.5

        # DONJA DESNA DIJAGONALA (middle+1 do pred-poslednje sa row=2*n)
        elif col > n and col < 2 * n and row == 2 * n:
            label = f"{polje.slovo}"
            #label_offset_x = size * 1.3
            label_offset_y = size * 1.5

        else:
            # Fallback
            continue

        text = font.render(label, True, (220, 220, 220))
        text_rect = text.get_rect(center=(cx + label_offset_x, cy + label_offset_y))
        screen.blit(text, text_rect)

    # Dodaj dodatne middle labele iznad prvog i ispod poslednjeg neegraničnog middle polja
    middle_polja = [p for p in tabla.raspored_polja
                    if p.slovo == middle_slovo and not p.granica]

    if middle_polja:
        # Najmanji broj (obično 1)
        prvi = min(middle_polja, key=lambda p: p.broj)
        q, r = tabla.koordinate_polja(prvi)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y - size * 3

        text = font.render(middle_slovo, True, (220, 220, 220))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)

        # Najveći broj
        poslednji = max(middle_polja, key=lambda p: p.broj)
        q, r = tabla.koordinate_polja(poslednji)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y + size * 3

        text = font.render(middle_slovo, True, (220, 220, 220))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)


def izracunaj_offset(tabla, size, screen_width, screen_height):
    """Izračunava offset za centriranje table na ekranu"""
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

    # Nacrtaj sva polja
    for polje in tabla.raspored_polja:
        nacrtaj_polje(screen, tabla, polje, size, offset_x, offset_y)

    # Nacrtaj labele van graničnih polja
    nacrtaj_labele(screen, tabla, size, offset_x, offset_y)

    return offset_x, offset_y