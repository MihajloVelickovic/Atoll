from collections import deque
from BitVector import BitVector
from src.models.ostrvo import Ostrvo
from src.enums.boje import Boje
from src.models.polje import Polje

class Tabla:
    def __init__(self, n):
        self.__n = n
        self.__uslov_pobede = 7 # broj ostrva / 2, broj ostrva je uvek 12
        self.__raspored_polja = []
        self.__putevi = [[[False for _ in range(5)] for _ in range(6)] for _ in range(2)]
        self.__ostrva = [Ostrvo() for _ in range(12)]
        self.__generisi_tablu()

    #region Pomocne funkcije, getteri, overrideovi

    # override za []
    def __getitem__(self, key):
        if type(key) != str:
            return None  # todo raise

        stripped = key.strip()
        if len(stripped) > 2 or len(stripped) < 1:
            return None  # todo raise

        if len(stripped) == 2:
            polje = \
            [x for x in self.__raspored_polja if x.slovo == stripped[0].capitalize() and x.broj == int(stripped[1])][0]
            index = self.__raspored_polja.index(polje)
            for o in self.__ostrva:
                if index in o.polja:
                    return o
            return polje
        else:
            if stripped.isdigit():
                return [x for x in self.__raspored_polja if x.broj == int(stripped[0])]
            elif stripped.isalpha():
                return [x for x in self.__raspored_polja if x.slovo == stripped[0].capitalize()]
            return None

    @property #pretvara metodu u atribut
    def raspored_polja(self):
        return self.__raspored_polja

    # getter za ostrva table
    @property
    def ostrva(self):
        return self.__ostrva

    @property
    def n(self):
        return self.__n

    @staticmethod
    def svi_moguci_potezi(stanje):
        return [i for i, x in enumerate(stanje[1:]) if x == 0]

    @staticmethod
    def sva_moguca_stanja(stanje):
        potezi = Tabla.svi_moguci_potezi(stanje)
        sva_moguca_stanja = []
        for potez in potezi:
            novo_stanje = stanje.deep_copy()
            novo_stanje[0] ^= 1
            novo_stanje[potez + 1] = 1
            sva_moguca_stanja.append(novo_stanje)

        return sva_moguca_stanja


    # Prikazuje informacije o tabli nakon generisanja
    def prikaz_polja(self):
        print("Polja:")
        for i in self.__raspored_polja:
            print(i.slovo, i.broj, i.boja, i.granica)

        print("Ostrva + susedi:")
        for i in self.__ostrva:
            polja = [self.__raspored_polja[x] for x in i.polja]
            susedi = [self.__raspored_polja[x] for x in range(0, len(self.__raspored_polja)) if x in i.susedi]
            print(polja,": ", susedi)

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

    def bit_vector(self, pairity):
        vec = BitVector(bitlist=[1 if x.boja == Boje.CRNA or x.boja == Boje.BELA else 0 for x in self.__raspored_polja])
        vec.pad_from_left(1)
        vec[0] = pairity
        return vec

    # vraca sva granicna polja table
    def granice(self):
        return [x for x in self.__raspored_polja if x.granica[0] is True]

    #endregion

    #region Generisanje table

    def __generisi_tablu(self):
        self.__generisi_sva_polja()
        self.__obrisi_nepostojece()
        self.__definisi_susedstva()
        self.__definisi_ostrva()
        self.__izbaci_polja_iz_suseda()

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
            self.__ostrva[index].boja = self.__raspored_polja[i].boja
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

    #endregion

    #region Provera pobede
    '''
    mozda nije najbolje ime
    ali funkcija je tablin deo odigravanja poteza
    znaci povezivanje ostrva ako je kliknuto polje susedno ostrvu,
    provera postojanja puteva izmedju ostrva te boje
    i provera da li je neki od tih puteva pobednicki
    '''
    def provera_pobede(self, kliknuto_polje):
        self.__povezi_ostrva(kliknuto_polje.susedi, kliknuto_polje.boja)
        putevi = self.__proveri_puteve(kliknuto_polje.boja)
        novi_put = self.__novi_put(putevi, kliknuto_polje.boja)
        return self.__pobeda(putevi, kliknuto_polje.boja, novi_put)

    # Postavlja o.povezano na true ako je kliknuto polje koje za suseda ima
    # polje koje pripada ostrvu iste boje kao potez koji je odigran
    def __povezi_ostrva(self, susedi, boja):
        looping = True
        for s in susedi:
            for o in self.__ostrva:
                if s in o.polja and o.povezano == False and boja == o.boja:
                    o.povezano = True
                    looping = False
                    break
            if not looping:
                break

    # True / False da li postoji put izmedju dva ostrva
    def __postoji_put(self, o1: Ostrvo, o2: Ostrvo, stampaj):
        if not o1.povezano or not o2.povezano or o1.boja != o2.boja:
            return False

        queue = deque()
        visited = []
        queue.extend(o1.susedi)
        while queue:
            susjed_index = queue.popleft()

            if susjed_index in visited:
                continue
            visited.append(susjed_index)

            susjed = self.__raspored_polja[susjed_index]
            if susjed.boja != o1.boja:
                continue

            if susjed_index in o2.polja:
                if stampaj:
                    print(f"{"C:" if o1.boja == Boje.CRNA else "B:"} "
                          f"{[self.__raspored_polja[x] for x in o1.polja]} "
                          f"<--> {[self.__raspored_polja[x] for x in o2.polja]}")
                return True

            queue.extend(susjed.susedi)

        return False

    '''
    funkcija formira listu listi boolova
    svaki bool predstavlja postojanje puta izmedju ostrva
    prva lista je prvo ostrvo te boje, druga drugo itd
    svaki element listi je bool koji predstavlja da li je ostrvo povezano sa 
    tim ostrvom za koje posmatramo bool
    primer: lista na polju [2] u skup_svih_puteva, za belu boju, je
    ostrvo sa indeksom [4] na listi ostrva, i moze da bude povezano sa ostrvima [0, 2, 6, 8 i 10]
    True / False u toj listi na polju sa indeksom [4] su onda redom da li je ostrvo povezano sa tim ostrvima
    '''
    def __proveri_puteve(self, boja):
        ostrva_date_boje = [idx for idx, x in enumerate(self.__ostrva) if x.boja == boja]
        skup_svih_puteva = []
        for i in range(0, len(ostrva_date_boje)):
            putevi_po_ostrvu = []
            index1 = ostrva_date_boje[i]
            for j in range(0, len(ostrva_date_boje)):
                if i == j:
                    continue
                putevi_index = 0 if boja == Boje.CRNA else 1
                # bool za stampanje u konzolu novih puteva
                # todo optimizacija
                stampaj_put = not self.__putevi[putevi_index][i][j-1]
                index2 = ostrva_date_boje[j]
                try:
                    postoji = (True if skup_svih_puteva[j][(i - 1) % 5] else
                               self.__postoji_put(self.__ostrva[index1], self.__ostrva[index2], stampaj_put))
                except IndexError:
                    postoji = self.__postoji_put(self.__ostrva[index1], self.__ostrva[index2], stampaj_put)

                putevi_po_ostrvu.append(postoji)
            skup_svih_puteva.append(putevi_po_ostrvu)
        return skup_svih_puteva

    # funkcija vraca true ako je povezan novi put
    # naznacava da treba da se odstamapju duzine obodnih puteva
    # todo optimizacija
    def __novi_put(self, putevi, boja):
        index = 0 if boja == Boje.CRNA else 1
        if not self.__putevi[index] or sorted(self.__putevi[index]) != sorted(putevi):
            self.__putevi[index] = putevi
            return True
        else:
            return False

    '''
    funkcija koja na osnovu boje igraca koji je odigrao potez
    i skupa svih postojecih puteva medju ostrvima
    odredjuje da li je igrac ispunio uslov pobede
    '''
    def __pobeda(self, svi_putevi, boja, novi_put):
        if not novi_put:
            return False

        # lista listi duzina obodnih puteva
        # funkcionise na principu disjunktnosti,
        # ako je ostrvo 0 povezano sa ostrvima 1 i 2
        # sve duzine obodnih puteva ce biti na indeksu 0 ove liste
        # dovoljno je da min element jedne od ovih listi ispuni uslov pobede
        # da zasigurno znamo da je igrac pobedio
        lista_duzina_obodnih_puteva = [[] for _ in range(6)]

        # prolaz kroz True / False liste postojanja puteva izmedju ostrva
        for i, putevi in enumerate(svi_putevi):

            # indeks trenutnog ostrva na listi svih ostrva (self.__ostrva)
            index_i = i * 2 + 1 if boja == Boje.CRNA else i * 2

            # svi indeski, i indeksi koji dolaze u obzir
            # prilikom provere duzine puta u smeru kazaljke na satu
            indeksi_clockwise_potrebni = [i % 12 for i in range(index_i + 2, index_i + 12, 2)]
            indeksi_clockwise_svi = [i % 12 for i in range(index_i, index_i + 12)]

            # svi indeski, i indeksi koji dolaze u obzir
            # prilikom provere duzine puta u smeru suprotnom kretanju kazaljke na satu
            indeksi_counter_clockwise_potrebni = [i % 12 for i in range(index_i - 2, index_i - 12, -2)]
            indeksi_counter_clockwise_svi = [i % 12 for i in range(index_i, index_i - 12,-1)]

            # pomocne liste gde se dodaju sve duzine za dato ostrvo
            # iz njih ce se izvuci maksimalna
            temp_lista_cw = []
            temp_lista_ccw = []

            # index liste u listi lista disjunktno povezanih ostrva ( :| )
            # u for petlji ispod se trazi najmanji indeks nekog ostrva povezanog
            # sa ostrvom j
            index_postojece_disjunktne_liste = index_i

            # ove dve liste su iste duzine, pa je sve jedno
            # kroz koju ce da se iterise
            for j in range(0, len(indeksi_clockwise_potrebni)):

                # indeksi (na listi svih ostrva) ostrva za koje trenutno proveravamo da li
                # su povezana sa ostrvom 'i' (spoljasnja petlja)
                # u oba smera
                index_cw = indeksi_clockwise_potrebni[j]
                index_ccw = indeksi_counter_clockwise_potrebni[j]

                # indeksi (na True / False listi postojanja puteva)
                # ostrva za koje trenutno proveravamo da li su povezana sa ostrvom 'i'
                # u oba smera
                index_ostrva_cw = (index_cw // 2 - (1 if index_cw > index_i else 0))
                index_ostrva_ccw = (index_ccw // 2 - (1 if index_ccw > index_i else 0))

                # ako je ostrvo povezano ->
                if putevi[index_ostrva_cw]:
                    if index_cw < index_postojece_disjunktne_liste:
                        index_postojece_disjunktne_liste = index_cw
                    # pozicije na listi svih ostrva u smeru kazaljke na satu
                    # koristi se za dobijanje duzine obodnog puta
                    pozicija_trenutnog = indeksi_clockwise_svi.index(index_i)
                    pozicija_trazenog = indeksi_clockwise_svi.index(index_cw)
                    duzina_obodnog_puta_cw = pozicija_trazenog - pozicija_trenutnog + 1
                    temp_lista_cw.append(duzina_obodnog_puta_cw)

                if putevi[index_ostrva_ccw]:
                    if index_ccw < index_postojece_disjunktne_liste:
                        index_postojece_disjunktne_liste = index_ccw
                    # pozicije na listi svih ostrva u smeru suprotnom kretanju kazaljke na satu
                    # koristi se za dobijanje duzine obodnog puta
                    pozicija_trenutnog = indeksi_counter_clockwise_svi.index(index_i)
                    pozicija_trazenog = indeksi_counter_clockwise_svi.index(index_ccw)
                    duzina_obodnog_puta_ccw = pozicija_trazenog - pozicija_trenutnog + 1
                    temp_lista_ccw.append(duzina_obodnog_puta_ccw)

            # ako su pomocne liste prazne nema sta da se dodaje
            if temp_lista_cw and temp_lista_ccw:
                # najmanji pronadjen indeks ostrva se pretvara u indeks za T/F listu
                # (lista listi disjunktno povezanih ostrva je iste strukture)
                index_postojece_disjunktne_liste = (index_postojece_disjunktne_liste // 2 -
                                                   (1 if index_postojece_disjunktne_liste > index_i else 0))
                lista_duzina_obodnih_puteva[index_postojece_disjunktne_liste].append(max(temp_lista_cw))
                lista_duzina_obodnih_puteva[index_postojece_disjunktne_liste].append(max(temp_lista_ccw))
                if novi_put:
                    print(f"{"C: " if boja == Boje.CRNA else "B: "}"
                          f"{[self.__raspored_polja[x] for x in self.__ostrva[index_i].polja]} "
                          f"CW: {lista_duzina_obodnih_puteva[index_postojece_disjunktne_liste][-2]} "
                          f"CCW: {lista_duzina_obodnih_puteva[index_postojece_disjunktne_liste][-1]}")

        # uslov pobede je da je minimalna duzina bilo kog obodnog puta
        # >= (broj_ostrva / 2) + 1
        for disjunktna_lista in lista_duzina_obodnih_puteva:
            if disjunktna_lista and min(disjunktna_lista) >= self.__uslov_pobede:
                return True

        return False

    #endregion