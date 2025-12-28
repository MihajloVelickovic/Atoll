class Polje:
    def __init__(self, slovo, broj, granica=False, boja = None):
        self.slovo = slovo
        self.broj = broj
        self.granica = granica
        self.susedi = []
        self.boja = boja

    def __eq__(self, other):
        if not isinstance(other, Polje):
            return False
        return (self.slovo == other.slovo and
                self.broj == other.broj)
