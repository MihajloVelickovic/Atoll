from src.models.polje import Polje


class Tabla:
    def __init__(self, n):
        self.n = n
        self.raspored_polja = []
        self.generisi_tablu()

    def generisi_tablu(self):
        korak = 0
        for i in range(0, 2 * self.n + 1):
            slovo = chr(ord('A') + ((ord('Z') - ord('A') + i) % 26))
            if i < self.n:
                for j in range(0, self.n + 1 + korak):
                    if i == 0 or j == self.n + korak or j == 0:
                        zauzeto = True
                        granica = True
                    else:
                        zauzeto = False
                        granica = False
                    self.raspored_polja.append(Polje(slovo=slovo, broj=j, zauzeto=zauzeto, granica=granica))
                korak += 1
            else:
                korak -= 1
                for j in range(i-self.n, 2*self.n+1):
                    if i == 0 or j == 2 * self.n or j == i - self.n:
                        zauzeto = True
                        granica = True
                    else:
                        zauzeto = False
                        granica = False
                    self.raspored_polja.append(Polje(slovo=slovo, broj=j, zauzeto=zauzeto, granica=granica))
        self.obrisi_nepostojece()
        self.definisi_susedstva()

    def obrisi_nepostojece(self):
        ids = []
        for idx, i in enumerate(range(0, 2*self.n + 1, self.n)):
            match idx:
                case 0:
                    ids = [0, self.n]
                case 1:
                    ids = [0, self.n * 2]
                case 2:
                    ids = [self.n, self.n * 2]
                case _:
                    return
            for j in ids:
                slovo = chr(ord('A') + ((ord('Z') - ord('A') + i) % 26))
                self.raspored_polja.remove(Polje(slovo=slovo, broj=j, zauzeto=True, granica=True))

    def prikaz_polja(self):
        for i in self.raspored_polja:
            print(i.slovo, i.broj, i.zauzeto)

    def definisi_susedstva(self):
        for polje in self.raspored_polja:
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
                    if sused in self.raspored_polja and sused != polje:
                        polje.susedi.append(self.raspored_polja.index(sused))

