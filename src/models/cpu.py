from random import randrange

from models.tabla import Tabla

class Cpu:

    @staticmethod
    def minimax(stanje, dubina, maksimizuje, alpha=float("-inf"), beta=float("inf")):

        # minimax je rekurzivna funkcija,
        # poziva se za svako stanje koje moze biti
        # sledece u odnosu na trenutno
        sva_sledeca_stanja = Tabla.sva_moguca_stanja(stanje)

        # kada dodjemo do listova stabla trazenja,
        # radimo staticku evaluaciju za cvor,
        # i funkcija vraca stanje i njegovu procenjenu vrednost
        if dubina == 0 or not sva_sledeca_stanja:
            return stanje, Cpu.proceni_stanje(stanje, True)

        # najbolje stanje je logicno
        # u pocetku stanje za koje pozivamo minimax
        najbolje_stanje = stanje

        # maksimizujuci deo, vraca stanje sa najvecom procenjenom vrednoscu
        if maksimizuje:
            max_vrednost = float("-inf")
            for sledece_stanje in sva_sledeca_stanja:
                # rekurzivni poziv za sledecu dubinu, ide se naizmenicno izmedju
                # maksimizovanja i minimizovanja
                vrednost = Cpu.minimax(sledece_stanje, dubina - 1, not maksimizuje, alpha, beta)

                # sustinski ce prvi put biti true jer je pocetna vrednost -inf
                # svakako je bilo koji potez bolji od najgoreg moguceg poteza
                if vrednost[1] > max_vrednost:
                    max_vrednost = vrednost[1]
                    najbolje_stanje = sledece_stanje

                alpha = max(alpha, vrednost[1])
                # naznacuje da zasigurno znamo da u nekoj od prethodno istrazenih grana
                # postoji bolji potez nego potezi koji bi na dalje bili proveravani
                if beta <= alpha:
                    break
            return najbolje_stanje, max_vrednost

        # maksimizujuci deo, vraca stanje sa najmanjom procenjenom vrednoscu
        # komentari iz maksimizujuceg dela se adekvatno odnose i na ovaj, samo
        # je min umesto max
        else:
            min_vrednost = float("inf")
            for sledece_stanje in sva_sledeca_stanja:

                vrednost = Cpu.minimax(sledece_stanje, dubina - 1, not maksimizuje, alpha, beta)

                if vrednost[1] < min_vrednost:
                    min_vrednost = vrednost[1]
                    najbolje_stanje = sledece_stanje

                beta = min(beta, vrednost[1])
                if alpha >= beta:
                    break

            return najbolje_stanje, min_vrednost

    @staticmethod
    def proceni_stanje(stanje, debug):
        if debug:
            return randrange(1,10)

        #TODO: uraditi pravu heuristiku lmao




        return None

