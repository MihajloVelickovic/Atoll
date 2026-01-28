class AI:

    @staticmethod
    def minimax(stanje, dubina, alpha, beta, maksimizuje):
        pass

    @staticmethod
    def heuristika(stanje):
        pass

    @staticmethod
    def najbolji_potez(igra):
        # TODO: implementirati minimax
        # za sada vraca prvi slobodan potez
        moguci_potezi = igra.svi_moguci_potezi()
        if moguci_potezi:
            return moguci_potezi[1]
        return None
