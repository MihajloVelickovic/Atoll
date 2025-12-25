class Polje:
    def __init__(self, slovo, broj, zauzeto=False, granica=False):
        self.slovo = slovo
        self.broj = broj
        self.zauzeto = zauzeto
        self.granica = granica
        self.susedi = []

    def __eq__(self, other):
        if not isinstance(other, Polje):
            return False
        return (self.slovo == other.slovo and
                self.broj == other.broj)
