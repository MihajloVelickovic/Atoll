class Ostrvo:
    def __init__(self):
        self.polja = []
        self.boja = None
        self.susedi = []
    def generisi_susede(self):
        for p in self.polja:
            for s in p.susedi:
                if s not in self.susedi:
                    self.susedi.append(s)

