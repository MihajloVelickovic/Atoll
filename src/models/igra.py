from src.enums.boje import Boje
from src.models.igrac import Igrac
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
        self.__initialized = True

    @classmethod
    def konstrukcija(cls):
        if cls.__instanca is not None:
            return cls.__instanca

        n = Igra.__unos_dimenzija()
        tip_partije = Igra.__unos_podataka_o_partiji("Odaberite vrstu igre:\n1. Covek v. Covek\n2. Covek v. CPU ")
        cpu_prvi = False
        if tip_partije:
           cpu_prvi = Igra.__unos_podataka_o_partiji("Odaberite prvog igraca:\n1. Covek\n2. CPU")

        beli_prvi = Igra.__unos_podataka_o_partiji("Odaberite prvog igraca:\n1. Crni\n2. Beli")

        beli_cpu = tip_partije and ((beli_prvi and cpu_prvi) or (not beli_prvi and not cpu_prvi))
        crni_cpu = tip_partije and not beli_cpu

        # p1 = Igrac(Boje.BELA, beli_cpu, beli_prvi)
        # p2 = Igrac(Boje.CRNA, crni_cpu, not beli_prvi)

        cls.__instanca = Igra(n, tip_partije, cpu_prvi, beli_prvi)
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
            Igra.__unos_dimenzija()

    @staticmethod
    def __unos_podataka_o_partiji(poruka):
        try:
            print()
            n = int(input(poruka))
            if  2 < n or n < 1:
                raise Exception("Morate uneti 0 (ne) ili 1 (da), pokusajte ponovo")
            return bool(n-1)
        except Exception as ex:
            print(ex)
            Igra.__unos_podataka_o_partiji(poruka)

