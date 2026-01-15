from src.enums.boje import Boje
from src.models.tabla import Tabla
from datetime import datetime

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
        self.kraj_igre = (False, False)
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

        beli_cpu = tip_partije and ((beli_prvi and cpu_prvi) or (not beli_prvi and not cpu_prvi))
        crni_cpu = tip_partije and not beli_cpu

        # p1 = Igrac(Boje.BELA, beli_cpu, beli_prvi)
        # p2 = Igrac(Boje.CRNA, crni_cpu, not beli_prvi)

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

    def odigraj_potez(self, kliknuto, originalna_boja, idx):
        if kliknuto:
            if kliknuto.boja != Boje.BEZ_TAMNA:
                print(f"Na polju {kliknuto.slovo}{kliknuto.broj} vec stoji kamencic")
                return False, originalna_boja

            kliknuto.boja = originalna_boja = Boje.BELA if self.trenutni_potez else Boje.CRNA
            self.trenutni_potez = not self.trenutni_potez
            print(f"Kliknuto: {kliknuto.slovo}{kliknuto.broj}")

            self.novo_stanje(idx)
            if self.tabla.provera_pobede(kliknuto):
                self.kraj_igre = (True, True)
                return True, kliknuto.boja

            if not self.ima_slobodnih_polja():
                self.kraj_igre = (True, False)
                return True, originalna_boja
            return True, originalna_boja
        return None, originalna_boja

    def novo_stanje(self, idx):
        self.stanja.append(self.stanja[-1].deep_copy())
        self.stanja[-1][idx + 1] = 1
        self.stanja[-1][0] ^= 1
        print(self.stanja[-1])

    def sacuvaj_izvestaj(self):
        with open(f"logs/{str(datetime.now())}.log", "x") as file:
            for stanje in self.stanja:
                file.write(str(stanje) + "\n")

    def ima_slobodnih_polja(self):
        return not self.stanja[-1][1:].count_bits() == self.stanja[-1][1:].length()