from random import randrange
class AI:

    @staticmethod
    def minimax(stanje, dubina, maksimizuje, alpha=float("-inf"), beta=float("inf")):

        sva_sledeca_stanja = AI.sva_moguca_stanja(stanje)

        if dubina == 0 or not sva_sledeca_stanja:
            return stanje, AI.heuristika(stanje)

        najbolje_stanje = stanje
        if maksimizuje:
            max_vrednost = float("-inf")
            for sledece_stanje in sva_sledeca_stanja:
                vrednost = AI.minimax(sledece_stanje, dubina-1, not maksimizuje, alpha, beta)

                if vrednost[1] > max_vrednost:
                    max_vrednost = vrednost[1]
                    najbolje_stanje = sledece_stanje

                alpha = max(alpha, vrednost[1])
                if beta <= alpha:
                    break
            return najbolje_stanje, max_vrednost

        else:
            min_vrednost = float("inf")

            for sledece_stanje in sva_sledeca_stanja:
                vrednost = AI.minimax(sledece_stanje, dubina-1, not maksimizuje, alpha, beta)

                if vrednost[1] < min_vrednost:
                    min_vrednost = vrednost[1]
                    najbolje_stanje = sledece_stanje

                beta = min(beta, vrednost[1])
                if alpha >= beta:
                    break

            return najbolje_stanje, min_vrednost

    @staticmethod
    def heuristika(stanje):
        #TODO: uraditi pravu heuristiku lmao
        return randrange(1,10)

    @staticmethod
    def svi_moguci_potezi(stanje):
        return [i for i, x in enumerate(stanje[1:]) if x == 0]

    @staticmethod
    def sva_moguca_stanja(stanje):
        potezi = AI.svi_moguci_potezi(stanje)
        sva_moguca_stanja = []
        for potez in potezi:
            novo_stanje = stanje.deep_copy()
            novo_stanje[0] ^= 1
            novo_stanje[potez+1]=1
            sva_moguca_stanja.append(novo_stanje)

        return sva_moguca_stanja