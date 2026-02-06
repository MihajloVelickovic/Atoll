from datetime import datetime

from gui.gui import Gui
from src.enums.boje import Boje
from src.models.cpu import Cpu
from src.models.tabla import Tabla

class Igra:

    __instanca = None

    def __new__(cls, *args, **kwargs):
        if cls.__instanca is None:
            cls.__instanca = super().__new__(cls)
        return cls.__instanca

    def __init__(self, n, cpu_partija=False, cpu_prvi=False, beli_prvi=True):
        if hasattr(self, "__initialized"):
            return
        self.tabla = Tabla(n)
        self.cpu_partija = cpu_partija
        self.cpu_prvi = cpu_prvi
        self.beli_prvi = beli_prvi
        self.stanja = [self.tabla.bit_vector(beli_prvi)]
        self.trenutni_potez = beli_prvi
        self.kraj_igre = (False, False) # (zavrsena_igra, zavrsena_pobedom)
        self.__initialized = True

    @property
    def get_dimenzije(self):
        return self.tabla.n

    @property
    def get_tabla(self):
        return self.tabla

    @classmethod
    def konstrukcija(cls):
        if cls.__instanca is not None:
            return cls.__instanca

        n = Igra.__unos_dimenzija()
        tip_partije = Igra.__unos_podataka_o_partiji("Odaberite vrstu igre:\n1. Covek v. Covek\n2. Covek v. CPU\n")
        cpu_prvi = False
        if tip_partije:
           cpu_prvi = Igra.__unos_podataka_o_partiji("Odaberite prvog igraca:\n1. Covek\n2. CPU\n")

        beli_prvi = Igra.__unos_podataka_o_partiji("Odaberite prvog igraca:\n1. Crni\n2. Beli\n")

        cls.__instanca = Igra(n, tip_partije, cpu_prvi, beli_prvi)
        return cls.__instanca

    @classmethod
    def debug_konstrukcija(cls, n, tip_partije, cpu_prvi, beli_prvi):
        cls.__instanca = Igra(n, tip_partije, cpu_prvi, beli_prvi )
        return cls.__instanca

    @classmethod
    def dekonstrukcija(cls):
        if cls.__instanca is not None:
            cls.__instanca = None

    @staticmethod
    def __unos_dimenzija():
        try:
            print("Unesite zeljenu dimenziju(3, 5, 7, 9) stranice table:")
            n = int(input())
            if n % 2 == 0 or 9 < n or n < 3:
                raise Exception("Dimenzija koju ste uneli nije validna, pokusajte ponovo")
            return n
        except Exception as ex:
            print(ex)
            return Igra.__unos_dimenzija()

    @staticmethod
    def __unos_podataka_o_partiji(poruka):
        try:
            print()
            n = int(input(poruka))
            if  2 < n or n < 1:
                raise Exception("Morate uneti 1 ili 2, pokusajte ponovo")
            return bool(n-1)
        except Exception as ex:
            print(ex)
            return Igra.__unos_podataka_o_partiji(poruka)

    def cpu_na_potezu(self):
        if not self.cpu_partija:
            return False
        cpu_je_beli = self.cpu_prvi == self.beli_prvi
        return self.trenutni_potez == cpu_je_beli

    def cpu_najbolji_potez(self):
        if not self.cpu_partija:
            return None
        najbolje_stanje = Cpu.minimax(self.stanja[-1], 3, True)
        potez = najbolje_stanje[0][1:] ^ self.stanja[-1][1:]
        return potez.next_set_bit()

    def odigraj_potez(self, kliknuto, originalna_boja, idx):
        if kliknuto:
            if kliknuto.boja not in (Boje.BEZ, Boje.BEZ_TAMNA):
                print(f"Na polju {kliknuto.slovo}{kliknuto.broj} vec stoji {"Beli" if kliknuto.boja == Boje.BELA else "Crni"} kamencic")
                return False, originalna_boja

            kliknuto.boja = originalna_boja = Boje.BELA if self.trenutni_potez else Boje.CRNA
            self.trenutni_potez = not self.trenutni_potez
            print(f"{"(CPU) " if not self.cpu_na_potezu() else ""}{"C: " if kliknuto.boja == Boje.CRNA else "B: "}{kliknuto.slovo}{kliknuto.broj}")

            self.novo_stanje(idx)
            if self.tabla.provera_pobede(kliknuto):
                print(f"{"(CPU) " if not self.cpu_na_potezu() else ""}{"C:" if kliknuto.boja == Boje.CRNA else "B:" } Pobeda")
                self.kraj_igre = (True, True)
                return True, kliknuto.boja

            if not self.ima_slobodnih_polja():
                self.kraj_igre = (True, False)
                return True, originalna_boja
            return True, originalna_boja
        return None, originalna_boja

    def odigraj_cpu_potez(self, gui: Gui):
        idx = self.cpu_najbolji_potez()
        polje = self.tabla.raspored_polja[idx]

        # nadam se temp fix ali videcemo....
        # problem je bio sto nakon odigranog poteza,
        # kada se mis pomeri s polja koje je kliknuto,
        # nakon cpu poteza bi se i ono obojilo u boju cpu igraca
        # to se desavalo zbog elegantno nepismenog nacina cuvanja i obrade
        # boja za razlicite dogadjaje u igri
        # ovaj fix u sustini simulira obradu hovera na polje koje ce ai da odigra
        # da bi se azurirala boja koju gui klasa cuva (posto se to menja i tokom odigravanja poteza i tokom hovera)
        gui.hover_logika(polje)
        if idx is not None:
            polje = self.tabla.raspored_polja[idx]
            _, gui.originalna_boja = self.odigraj_potez(polje, gui.originalna_boja, idx)

    def novo_stanje(self, idx):
        if self.stanja[-1][idx + 1] == 1:
            return
        self.stanja.append(self.stanja[-1].deep_copy())
        self.stanja[-1][idx + 1] = 1
        self.stanja[-1][0] ^= 1

    def sacuvaj_izvestaj(self, kraj_igre):
        vreme_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"src/logs/{vreme_string}.log"
        print(f"Izvestaj igre sacuvan u: {file_name}")
        with open(file_name, "x") as file:
            file.write("IZVESTAJ\n")
            potez = "POCETNO_STANJE"
            prethodno = None
            for stanje in self.stanja:
                if prethodno is not None:
                    # stanja se uvek razlikuju za 1 bit, kog xorovanje izvlaci
                    promena = stanje[1:] ^ prethodno[1:]
                    # fja vraca poziciju prvog postavljenog bita, a ima samo 1 nakon xora
                    index = promena.next_set_bit()
                    # (index u bitvektoru) + 1 je jednak indeksu polja u tabla.__raspored_polja
                    # - 1 nije potrebno jer je prvi bit iskljucen iz xorovanja
                    potez = str(self.tabla.raspored_polja[index])
                    potez = f"{"C: " if ko_je_igrao == 0 else "B: "}" + potez
                file.write(str(stanje) + "\t" + potez + "\n")
                # prvi bit predstavlja igraca
                ko_je_igrao = stanje[0]
                prethodno = stanje

            poslednja_linija = ("IGRA_PREKINUTA" if not kraj_igre[0] else
                                f"{"CRNI" if ko_je_igrao == 1 else "BELI"}_POBEDIO" if kraj_igre[1] else
                                "NEMA_SLOBODNIH_POLJA")
            file.write(poslednja_linija)

    def ima_slobodnih_polja(self):
        # count_bits vraca broj postavljenih bitova, ako ih ima isto koliko ima bitova
        # ukupno onda nema slobodnih polja
        return not self.stanja[-1][1:].count_bits() == self.stanja[-1][1:].length()
