from random import randrange
class AI:

    @staticmethod
    def minimax(stanje, dubina, maksimizuje, alpha=(None, float("-inf")), beta=(None, float("inf"))):
        if maksimizuje:
            return AI.max_f(stanje, dubina, alpha, beta)
        else:
            return AI.min_f(stanje, dubina, alpha, beta)

    @staticmethod
    def heuristika(stanje):
        return randrange(1,10)

    @staticmethod
    def max_f(stanje, dubina, alpha, beta):
        nova_stanja = AI.sva_moguca_stanja(stanje)
        if dubina == 0 or not nova_stanja:
            return stanje, AI.heuristika(stanje)
        else:
            for s in nova_stanja:
                alpha = max(alpha, AI.min_f(s, dubina-1, alpha, beta), key=lambda x: x[1])
                if alpha >= beta:
                    return beta
        return alpha

    @staticmethod
    def min_f(stanje, dubina, alpha, beta):
        nova_stanja = AI.sva_moguca_stanja(stanje)
        if dubina == 0 or not nova_stanja:
            return stanje, AI.heuristika(stanje)
        else:
            for s in nova_stanja:
                alpha = min(alpha, AI.max_f(s, dubina - 1, alpha, beta), key=lambda x: x[0])
                if beta <= alpha:
                    return alpha
        return beta

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