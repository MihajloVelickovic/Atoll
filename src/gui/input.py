from src.gui.renderer import koordinate_polja
from src.enums.boje import Boje
from math import pi, sin, cos

def nadji_kliknuto_polje(clicked_position, tabla, size_x, size_y, offset_x, offset_y):
    clicked_x, clicked_y = clicked_position

    for polje in tabla.raspored_polja:
        x, y = koordinate_polja(polje, tabla, size_x, offset_x, offset_y)
        vx = []
        vy = []
        angle = 0
        while angle < 360:
            rotirana_tacka = rotiraj_tacku(x - size_x, y, x, y, angle)
            vx.append(rotirana_tacka[0])
            vy.append(rotirana_tacka[1])
            angle += 60

        if tacka_u_poligonu(6, vx, vy, clicked_x, clicked_y):
            return polje

    return None

# https://stackoverflow.com/a/2212851/30315841
# adaptiran u python funkciju
# shaut aut za dragog stranca
def tacka_u_poligonu(nvert, vertx, verty, testx, testy):
    i = j = c = False
    j = nvert - 1
    for i in range(0, nvert):
        if( ( ( verty[i] > testy ) != ( verty[j] > testy ) ) and
            ( testx < ( vertx[j] - vertx[i] ) * ( testy - verty[i] ) / ( verty[j] - verty[i] ) + vertx[i] ) ):
            c = not c
        j = i
    return c

# (xbase, ybase) je tacka oko koje se rotira tacka (x, y)
# rotacija kontra kazaljki na satu :D
def rotiraj_tacku(x, y, xbase, ybase, angle):
    new_coord = transliraj_tacku(x, y, -xbase, -ybase)[0:2]
    angle_rad = angle * pi / 180
    rotmat = [[cos(angle_rad), sin(angle_rad)], [-sin(angle_rad),  cos(angle_rad)]]
    rot_coord = [0, 0]

    for i, row in enumerate(rotmat):
        for j, p in enumerate(new_coord):
            rot_coord[i] += p * row[j]

    return transliraj_tacku(rot_coord[0], rot_coord[1], xbase, ybase)[0:2]

# translira tacku (x, y) za (tx, ty)
def transliraj_tacku(x, y, tx, ty):
    point = [x, y, 1]
    matrix = [[1, 0, tx], [0, 1, ty],[0, 0, 1]]
    new_coord = [0, 0, 0]
    for i, row in enumerate(matrix):
        for j, p in enumerate(point):
            new_coord[i] += p * row[j]
    return new_coord


def primeni_hover_efekat(polje):
    """Primenjuje hover boju na polje i vraća originalnu boju."""
    if polje is None:
        return None

    originalna_boja = polje.boja
    if polje.boja == Boje.BEZ:
        polje.boja = Boje.BEZ_TAMNA
    elif polje.boja == Boje.CRNA:
        polje.boja = Boje.TAMNOSIVA
    elif polje.boja == Boje.BELA:
        polje.boja = Boje.SVETLOSIVA

    return originalna_boja


def ukloni_hover_efekat(polje, originalna_boja):
    """Vraća originalnu boju polju."""
    if polje is not None and originalna_boja is not None:
        polje.boja = originalna_boja

