class Polje:
    def __init__(self, slovo, broj, granica=False, ostrvo=None, boja=None):
        self.slovo = slovo
        self.broj = broj
        self.granica = (granica, ostrvo)
        self.susedi = []
        self.boja = boja

    def __eq__(self, other):
        if not isinstance(other, Polje):
            return False
        return (self.slovo == other.slovo and
                self.broj == other.broj)

    def __repr__(self):
        return self.slovo + str(self.broj)
