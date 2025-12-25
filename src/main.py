from src.models.tabla import Tabla

a = Tabla(7)

#a.prikaz_polja()

for i in a.raspored_polja[18:19]:
    for s in i.susedi:
        print(a.raspored_polja[s].slovo, a.raspored_polja[s].broj)
