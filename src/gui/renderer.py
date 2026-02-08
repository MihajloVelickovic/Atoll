import pygame
import math

from src.enums.boje import Boje


# konvertuje axial koordinate u pixel koordinate
# flattop orijentacija (ravna ivica gore/dole)
def axial_to_pixel(q, r, size):
    x = size * (3 / 2 * q)
    y = size * (math.sqrt(3) / 2 * q + math.sqrt(3) * r)
    return x, y


# vraca pixel koordinate centra polja na ekranu
def koordinate_polja(polje, tabla, size, offset_x, offset_y):
    q, r = tabla.koordinate_polja(polje)
    x, y = axial_to_pixel(q, r, size)
    return x + offset_x, y + offset_y


# crta jedno heksagonalno polje (flattop orijentacija)
def nacrtaj_polje(screen, tabla, polje, size, offset_x, offset_y, labele):
    q, r = tabla.koordinate_polja(polje)
    x, y = axial_to_pixel(q, r, size)
    cx = x + offset_x
    cy = y + offset_y

    # crtanje hexagona
    points = []
    for i in range(6):
        angle = math.pi / 3 * i  # bez rotacije za flattop
        px = cx + size * math.cos(angle)
        py = cy + size * math.sin(angle)
        points.append((px, py))

    color = polje.boja.value
    pygame.draw.polygon(screen, color, points)
    # crtanje ivice
    pygame.draw.polygon(screen, (100, 90, 70), points, 2)

    # oznaka polja
    if not polje.granica[0] and labele:
        font = pygame.font.Font(None, 18)
        label = f"{polje.slovo}{polje.broj}"
        text = font.render(label, True, (60, 60, 60))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)


# crta labele (slova i brojeve) van granicnih polja
def nacrtaj_labele(screen, tabla, size, offset_x, offset_y):
    font = pygame.font.Font(None, 22)

    n = tabla.n

    # dinamicki odredi slovo za red u sredini (G za n=7, E za n=5, C za n=3)
    # Z je kolona 0, A je kolona 1, middle je kolona n
    srednja_kolona_slovo = chr(ord('Z') + n) if n == 0 else chr(ord('A') + n - 1)

    # prvo nacrtaj labele za granicna polja
    for polje in tabla.raspored_polja:
        if not polje.granica:
            continue

        q, r = tabla.koordinate_polja(polje)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y

        label_offset_x, label_offset_y = 0, 0

        col = 0 if polje.slovo == 'Z' else ord(polje.slovo) - ord('A') + 1
        row = polje.broj

        # leva vertikala (Z kolona) - brojevi levo
        if polje.slovo == 'Z':
            label = f"{polje.broj}"
            label_offset_x = -size * 1.5
            label_offset_y = size * 0.8

        # desna vertikala (N kolona) - brojevi desno
        elif col == 2 * n:  # Dinamički - poslednja kolona
            label = f"{polje.broj}"
            label_offset_x = size * 1.5
            label_offset_y = -size * 0.8

        # gornja leva dijagonala (A do middle-1 sa row=0)
        elif row == 0 and 1 <= col < n:
            label = f"{polje.slovo}"
            # label_offset_x = -size * 1.3
            label_offset_y = -size * 1.5

        # vrh (middle slovo sa row=0)
        elif row == 0 and col == n:
            label = f"{polje.slovo}"
            label_offset_y = -size * 1.5

        # gornja desna dijagonala (middle+1 do pretposlednje kolone gde je row=col-n)
        elif n < col < 2 * n and row == col - n:
            label = f"{polje.slovo}"
            label_offset_y = -size * 1.5

        # donja leva dijagonala (A do middle-1 gde je row=n+col)
        elif 1 <= col < n and row == n + col:
            label = f"{polje.slovo}"
            label_offset_y = size * 1.5

        # dno (middle slovo sa row=2*n)
        elif col == n and row == 2 * n:
            label = f"{polje.slovo}"
            label_offset_y = size * 1.5

        # donja desna dijagonala (middle + 1 do pretposlednje sa row=2*n)
        elif n < col < 2 * n and row == 2 * n:
            label = f"{polje.slovo}"
            label_offset_y = size * 1.5

        else:
            continue

        text = font.render(label, True, (220, 220, 220))
        text_rect = text.get_rect(center=(cx + label_offset_x, cy + label_offset_y))
        screen.blit(text, text_rect)

    # dodavanje dodatne labele iznad prvog i ispod poslednjeg negranicnog srednjeg polja
    srednja_kolona_polja = [p for p in tabla.raspored_polja
                            if p.slovo == srednja_kolona_slovo and not p.granica]

    if srednja_kolona_polja:
        # najmanji broj (obicno 1)
        prvi = min(srednja_kolona_polja, key=lambda p: p.broj)
        q, r = tabla.koordinate_polja(prvi)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y - size * 3

        text = font.render(srednja_kolona_slovo, True, (220, 220, 220))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)

        # najveci broj
        poslednji = max(srednja_kolona_polja, key=lambda p: p.broj)
        q, r = tabla.koordinate_polja(poslednji)
        x, y = axial_to_pixel(q, r, size)
        cx = x + offset_x
        cy = y + offset_y + size * 3

        text = font.render(srednja_kolona_slovo, True, (220, 220, 220))
        text_rect = text.get_rect(center=(cx, cy))
        screen.blit(text, text_rect)


# izracunava offset za centriranje table na ekranu
def izracunaj_offset(tabla, size, screen_width, screen_height):
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

    # dodavanje margina
    table_width = max_x - min_x + 3 * size
    table_height = max_y - min_y + 3 * size

    offset_x = (screen_width - table_width) / 2 - min_x + 1.5 * size
    offset_y = (screen_height - table_height) / 2 - min_y + 1.5 * size

    return offset_x, offset_y


def nacrtaj_tablu(screen, tabla, size=30, labele=False):
    # crta celu tablu sa automatskim centriranjem
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    offset_x, offset_y = izracunaj_offset(tabla, size, screen_width, screen_height)

    # crtanje svih polja
    for polje in tabla.raspored_polja:
        nacrtaj_polje(screen, tabla, polje, size, offset_x, offset_y, labele)

    # crtanje labela van granicnih polja
    nacrtaj_labele(screen, tabla, size, offset_x, offset_y)

    return offset_x, offset_y


# prikazuje tekstualnu poruku preko celog ekrana
def prikazi_text_overlay(screen, text):
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(180)
    overlay.fill((10, 10, 50))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 50)
    text_color = (255, 255, 100)

    text = font.render(text, True, text_color)
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, rect)


def prikazi_kraj_nema_slobodnih(screen):
    text = "Kraj igre. Nema više slobodnih polja."
    prikazi_text_overlay(screen, text)


def prikazi_kraj_pobeda(screen, pobednik):
    text = f"Kraj igre. {"Crni" if pobednik == Boje.CRNA else "Beli"} igrač je pobedio."
    prikazi_text_overlay(screen, text)
