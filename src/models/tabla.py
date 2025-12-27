from src.enums.boje import Boje
from src.models.polje import Polje

class Tabla:
    def __init__(self, n):
        self.__n = n
        self.__raspored_polja = []
        self.__generisi_tablu()

    def __generisi_tablu(self):
        self.__generisi_sva_polja()
        self.__obrisi_nepostojece()
        self.__definisi_susedstva()

    @property #pretvara metodu u atribut
    def get_raspored_polja(self):
        return self.__raspored_polja

    @property #pretvara metodu u atribut
    def n(self):
        return self.__n

    def __generisi_sva_polja(self):
        korak = 0
        # for petlja po slovima od Z (A-1) do A+2*n
        for i in range(0, 2 * self.__n + 1):
            # mora ovako da bi slovo preslo sa Z na A kada poraste I
            slovo = chr(ord('A') + ((ord('Z') - ord('A') + i) % 26))
            # prvi if, zaduzen za levu polovinu table, kada sa svakim slovom raste broj polja u koloni
            if i < self.__n:
                # brojevi od 0 do potrebnog za kolonu
                for j in range(0, self.__n + 1 + korak):
                    # slovo Z, uvek granicno
                    if i == 0:
                        granica = True
                        # prva polovina redova (brojeva)
                        if j < (self.__n + 1)/2:
                            boja = Boje.CRNA
                        # druga polovina redova (brojeva)
                        else:
                            boja = Boje.BELA

                    # prvi prvcati red na tabli, onaj gde su
                    # vec postavljeni kamencici pre pocetka igre
                    elif j == 0:
                        granica = True
                        # prva polovina kolona (slova)
                        if i < (self.__n + 1) / 2:
                            boja = Boje.BELA
                        # druga polovina kolona (slova)
                        else:
                            boja = Boje.CRNA

                    # isti slucaj kao prosli if ali poslednji red
                    elif j == self.__n + korak:
                        granica = True
                        if i < (self.__n + 1) / 2:
                            boja = Boje.CRNA
                        else:
                            boja = Boje.BELA

                    # sva polja sa prve polovine table koja nisu krajnja
                    # to jest, sva slobodna polja kada igra pocne
                    else:
                        boja = None
                        granica = False

                    self.__raspored_polja.append(Polje(slovo=slovo, broj=j, granica=granica, boja=boja))
                korak += 1

            # sve isto kao prosli if, ali druga polovina table, kada opadaju redovi svakoj koloni
            else:
                korak -= 1
                for j in range(i - self.__n, 2 * self.__n + 1):

                    if i == 2 * self.__n:
                        granica = True
                        if j < self.__n + (self.__n + 1)/2:
                            boja = Boje.BELA
                        else:
                            boja = Boje.CRNA

                    elif j == i - self.__n:
                        granica = True
                        if i < self.__n + (self.__n + 1) / 2:
                            boja = Boje.BELA
                        else:
                            boja = Boje.CRNA

                    elif j == 2 * self.__n:
                        granica = True
                        if i < self.__n + (self.__n + 1) / 2:
                            boja = Boje.CRNA
                        else:
                            boja = Boje.BELA

                    else:
                        boja = None
                        granica = False

                    self.__raspored_polja.append(Polje(slovo=slovo, broj=j, granica=granica, boja=boja))

    def __obrisi_nepostojece(self):
        ids = []
        for idx, i in enumerate(range(0, 2 * self.__n + 1, self.__n)):
            match idx:
                case 0:
                    ids = [0, self.__n]
                case 1:
                    ids = [0, self.__n * 2]
                case 2:
                    ids = [self.__n, self.__n * 2]
                case _:
                    return
            for j in ids:
                slovo = chr(ord('A') + ((ord('Z') - ord('A') + i) % 26))
                self.__raspored_polja.remove(Polje(slovo=slovo, broj=j))

    def prikaz_polja(self):
        for i in self.__raspored_polja:
            print(i.slovo, i.broj, i.boja, i.granica)

    def __definisi_susedstva(self):
        for polje in self.__raspored_polja:
            for i in range(-1, 2):
                if i == -1:
                    ids = [-1, 0]
                elif i == 0:
                    ids = [-1, 1]
                elif i == 1:
                    ids = [0, 1]
                else:
                    return

                for j in ids:
                    slovo = chr(ord('A') + ((ord(polje.slovo) - ord('A') + i) % 26))
                    sused = Polje(slovo = slovo, broj = polje.broj+j)
                    if sused in self.__raspored_polja and sused != polje:
                        polje.susedi.append(self.__raspored_polja.index(sused))

    def koordinate_polja(self, polje):
        # Slovo -> col
        if polje.slovo == 'Z':
            col = 0
        else:
            col = ord(polje.slovo) - ord('A') + 1

        row = polje.broj

        q = col - self.__n
        r = row - col

        return q, r