from collections import deque
from typing import List

from models.ostrvo import Ostrvo
from src.enums.boje import Boje
from src.models.polje import Polje

class Tabla:
    def __init__(self, n):
        self.__n = n
        self.__raspored_polja = []
        self.__ostrva = [Ostrvo() for _ in range(12)]
        self.__generisi_tablu()

    def __generisi_tablu(self):
        self.__generisi_sva_polja()
        self.__obrisi_nepostojece()
        self.__definisi_susedstva()
        self.__definisi_ostrva()
        self.__izbaci_polja_iz_suseda()

    def __getitem__(self, key):
        if type(key) != str:
            return None #todo raise

        stripped = key.strip()
        if len(stripped) > 2 or len(stripped) < 1:
            return None #todo raise

        if len(stripped) == 2:
            return [x for x in self.__raspored_polja if x.slovo == stripped[0].capitalize() and x.broj == int(stripped[1])][0]
        else:
            if stripped.isdigit():
                return [x for x in self.__raspored_polja if x.broj == int(stripped[0])]
            elif stripped.isalpha():
                return [x for x in self.__raspored_polja if x.slovo == stripped[0].capitalize()]
            return None

    def granice(self):
        return [x for x in self.__raspored_polja if x.granica[0] is True]

    @property #pretvara metodu u atribut
    def raspored_polja(self):
        return self.__raspored_polja

    @property
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
                    ostrvo = None
                    # slovo Z, uvek granicno
                    if i == 0:
                        granica = True
                        # prva polovina redova (brojeva)
                        if j < (self.__n + 1)/2:
                            boja = Boje.CRNA
                            ostrvo = 11
                        # druga polovina redova (brojeva)
                        else:
                            boja = Boje.BELA
                            ostrvo = 10

                    # prvi prvcati red na tabli, onaj gde su
                    # vec postavljeni kamencici pre pocetka igre
                    elif j == 0:
                        granica = True
                        # prva polovina kolona (slova)
                        if i < (self.__n + 1) / 2:
                            boja = Boje.BELA
                            ostrvo = 0
                        # druga polovina kolona (slova)
                        else:
                            boja = Boje.CRNA
                            ostrvo = 1

                    # isti slucaj kao prosli if ali poslednji red
                    elif j == self.__n + korak:
                        granica = True
                        if i < (self.__n + 1) / 2:
                            boja = Boje.CRNA
                            ostrvo = 9
                        else:
                            boja = Boje.BELA
                            ostrvo = 8

                    # sva polja sa prve polovine table koja nisu krajnja
                    # to jest, sva slobodna polja kada igra pocne
                    else:
                        boja = Boje.BEZ
                        granica = False

                    self.__raspored_polja.append(Polje(slovo=slovo, broj=j, granica=granica, ostrvo=ostrvo, boja=boja))
                korak += 1

            # sve isto kao prosli if, ali druga polovina table, kada opadaju redovi svakoj koloni
            else:
                korak -= 1
                for j in range(i - self.__n, 2 * self.__n + 1):
                    ostrvo = None
                    if i == 2 * self.__n:
                        granica = True
                        if j < self.__n + (self.__n + 1)/2:
                            boja = Boje.BELA
                            ostrvo = 4
                        else:
                            boja = Boje.CRNA
                            ostrvo = 5

                    elif j == i - self.__n:
                        granica = True
                        if i < self.__n + (self.__n + 1) / 2:
                            boja = Boje.BELA
                            ostrvo = 2
                        else:
                            boja = Boje.CRNA
                            ostrvo = 3

                    elif j == 2 * self.__n:
                        granica = True
                        if i < self.__n + (self.__n + 1) / 2:
                            boja = Boje.CRNA
                            ostrvo = 7
                        else:
                            boja = Boje.BELA
                            ostrvo = 6

                    else:
                        boja = Boje.BEZ
                        granica = False

                    self.__raspored_polja.append(Polje(slovo=slovo, broj=j, granica=granica, ostrvo=ostrvo,boja=boja))

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

    def __definisi_ostrva(self):
        granice = self.granice()
        for granicar in granice:
            # index ostrva gde se nalazi granicar
            index = granicar.granica[1]
            # index granicara polja u rasporedu polja
            i = self.__raspored_polja.index(granicar)
            # dodavanje granicnih polja u korektno ostrvo
            self.__ostrva[index].polja.append(i)
            # dodavanje suseda ostrvskih polja u listu suseda
            for s in self.__raspored_polja[i].susedi:
                if s not in self.__ostrva[index].susedi:
                    self.__ostrva[index].susedi.append(s)

    # izbacivanje samih ostrvskih polja iz sopstvene liste suseda
    def __izbaci_polja_iz_suseda(self):
        for o in self.__ostrva:
            removal_list = []
            for s in o.susedi:
                if s in o.polja:
                    removal_list.append(s)
            for r in removal_list:
                o.susedi.remove(r)

    def prikaz_polja(self):
        print("Polja:")
        for i in self.__raspored_polja:
            print(i.slovo, i.broj, i.boja, i.granica)

        print("Ostrva + susedi:")
        for i in self.__ostrva:
            polja = [self.__raspored_polja[x] for x in i.polja]
            susedi = [self.__raspored_polja[x] for x in range(0, len(self.__raspored_polja)) if x in i.susedi]
            print(polja,": ", susedi)

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

    def postoji_put(self, ostrvo1, ostrvo2):
        return
