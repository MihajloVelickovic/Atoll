class Polje:
    def __init__(self, slovo, broj, zauzeto=False, granica=False):
        self.slovo = slovo
        self.broj = broj
        self.zauzeto = zauzeto
        self.granica = granica

    def __eq__(self, other):
        if not isinstance(other, Polje):
            return False
        return (self.slovo == other.slovo and
                self.broj == other.broj and
                self.zauzeto == other.zauzeto and
                self.granica == other.granica)
