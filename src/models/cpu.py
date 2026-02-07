from src.models.tabla import Tabla
from src.enums.boje import Boje

class Cpu:

    DUBINA = 4
    DEBUG = True

    # indeks najboljeg poteza i njegova vrednost
    # sustinski omotac oko minimaxa
    @staticmethod
    def najbolji_potez(tabla, cpu_boja):
        vrednost, potez = Cpu.minimax(tabla, Cpu.DUBINA, True, cpu_boja, float("-inf"), float("inf"))
        if Cpu.DEBUG:
            polje = tabla.raspored_polja[potez] if potez is not None else None
            if polje:
                print(f"[CPU] Najbolji potez: {polje.slovo if polje else '?'}{polje.broj if polje else '?'} (vrednost = {vrednost})")
        return potez

    # minimax sa alfa beta odsecanjem
    @staticmethod
    def minimax(tabla, dubina, maksimizuje, cpu_boja, alpha, beta):
        protivnik_boja = Boje.CRNA if cpu_boja == Boje.BELA else Boje.BELA
        trenutna_boja = cpu_boja if maksimizuje else protivnik_boja

        moguci_potezi = tabla.svi_moguci_potezi_idx()

        # izlazak iz rekurzije
        if dubina == 0 or not moguci_potezi:
            return Cpu.heuristika(tabla, cpu_boja), None

        najbolji_potez_idx = moguci_potezi[0]

        # maksimizujuci deo minimaxa
        if maksimizuje:
            max_vrednost = float("-inf")
            for potez_idx in moguci_potezi:
                # simulacija odigravanja poteza, ali bez propratnih efekata
                tabla.primeni_potez_simulacija(potez_idx, trenutna_boja)

                # provera pobede simuliranog poteza
                if tabla.provera_pobede_simulacija(trenutna_boja):
                    tabla.ponisti_potez(potez_idx)
                    return 10000, potez_idx

                vrednost, _ = Cpu.minimax(tabla, dubina - 1, False, cpu_boja, alpha, beta)

                # ponistavanje simuliranog poteza
                tabla.ponisti_potez(potez_idx)

                if vrednost > max_vrednost:
                    max_vrednost = vrednost
                    najbolji_potez_idx = potez_idx

                # alfa beta odsecanje
                alpha = max(alpha, vrednost)
                if beta <= alpha:
                    break

            # Ako nismo nasli nista bolje od -inf, uzmi prvi potez
            if max_vrednost == float("-inf"):
                return 0, najbolji_potez_idx

            return max_vrednost, najbolji_potez_idx

        # minimizujuci deo minimaxa
        else:
            min_vrednost = float("inf")
            for potez_idx in moguci_potezi:
                tabla.primeni_potez_simulacija(potez_idx, trenutna_boja)

                if tabla.provera_pobede_simulacija(trenutna_boja):
                    tabla.ponisti_potez(potez_idx)
                    return -10000, potez_idx

                vrednost, _ = Cpu.minimax(tabla, dubina - 1, True, cpu_boja, alpha, beta)

                tabla.ponisti_potez(potez_idx)

                if vrednost < min_vrednost:
                    min_vrednost = vrednost
                    najbolji_potez_idx = potez_idx

                # alfa beta odsecanje
                beta = min(beta, vrednost)
                if alpha >= beta:
                    break

            # Ako nismo nasli nista bolje od inf, uzmi prvi potez
            if min_vrednost == float("inf"):
                return 0, moguci_potezi[0]

            return min_vrednost, najbolji_potez_idx


    # procenjuje vrednost stanja
    @staticmethod
    def heuristika(tabla, cpu_boja):
        protivnik_boja = Boje.CRNA if cpu_boja == Boje.BELA else Boje.BELA
        score = 0

        # broj aktivnih ostrva (imaju kamencic uz sebe)
        cpu_aktivna = Cpu._broji_aktivna_ostrva(tabla, cpu_boja)
        protivnik_aktivna = Cpu._broji_aktivna_ostrva(tabla, protivnik_boja)

        score += cpu_aktivna * 30
        score -= protivnik_aktivna * 30

        # broj kamencica koji su uz ostrva (podsticanje pocetka gradnje)
        cpu_uz_ostrva = Cpu._broji_kamencice_uz_ostrva(tabla, cpu_boja)
        protivnik_uz_ostrva = Cpu._broji_kamencice_uz_ostrva(tabla, protivnik_boja)

        score += cpu_uz_ostrva * 20
        score -= protivnik_uz_ostrva * 20

        # bonus za duzinu lanaca koji krecu od ostrva
        cpu_duzina_lanaca = Cpu._ukupna_duzina_lanaca(tabla, cpu_boja)
        protivnik_duzina_lanaca = Cpu._ukupna_duzina_lanaca(tabla, protivnik_boja)

        score += cpu_duzina_lanaca * 15
        score -= protivnik_duzina_lanaca * 15

        # evaluacija spojenih parova ostrva
        # uzima u obzir duzinu obodnog puta
        cpu_score_parovi = Cpu._evaluiraj_spojene_parove(tabla, cpu_boja)
        protivnik_score_parovi = Cpu._evaluiraj_spojene_parove(tabla, protivnik_boja)

        score += cpu_score_parovi
        score -= protivnik_score_parovi

        return score

    # racuna ukupnu duzinu svih lanaca koji krecu od ostrva date boje
    # duzi lanac znaci da je ostrvo blize spajanju s drugim ostrvom
    @staticmethod
    def _ukupna_duzina_lanaca(tabla, boja):
        from collections import deque

        ukupna_duzina = 0

        # da ne brojimo isti kamencic vise puta
        visited_global = set()

        for o in tabla.ostrva:
            if o.boja != boja:
                continue

            # BFS od ovog ostrva da nadjemo sve povezane kamencice
            queue = deque()
            visited = set()

            for s_idx in o.susedi:
                if tabla.raspored_polja[s_idx].boja == boja:
                    queue.append(s_idx)

            while queue:
                idx = queue.popleft()
                if idx in visited or idx in visited_global:
                    continue
                visited.add(idx)

                polje = tabla.raspored_polja[idx]
                if polje.boja != boja:
                    continue

                ukupna_duzina += 1

                for s_idx in polje.susedi:
                    if s_idx not in visited and s_idx not in visited_global:
                        queue.append(s_idx)

            visited_global.update(visited)

        return ukupna_duzina

    # broji kamencice date boje koji su direktno uz ostrvo iste boje
    @staticmethod
    def _broji_kamencice_uz_ostrva(tabla, boja):
        count = 0
        for o in tabla.ostrva:
            if o.boja != boja:
                continue
            for s_idx in o.susedi:
                if tabla.raspored_polja[s_idx].boja == boja:
                    count += 1
        return count

    # evaluira spojene parove ostrva za datu boju
    # veca vrednost za parove koji su blizi pobednickoj duzini
    @staticmethod
    def _evaluiraj_spojene_parove(tabla, boja):
        ostrva_boje = [o for o in tabla.ostrva if o.boja == boja]
        score = 0
        uslov_pobede = 7  # broj ostrva / 2 + 1

        for i, o1 in enumerate(ostrva_boje):
            for o2 in ostrva_boje[i+1:]:
                if Cpu._postoji_put_izmedju(tabla, o1, o2):
                    # duzina najmanjeg obodnog puta izmedju ostrva
                    idx1 = tabla.ostrva.index(o1)
                    idx2 = tabla.ostrva.index(o2)
                    duzina = Tabla.duzina_obodnog_puta(idx1, idx2)

                    if duzina >= uslov_pobede:
                        # pobednicki par, ogroman bonus
                        score += 5000
                    elif duzina == uslov_pobede - 1:
                        # jedan korak do pobede
                        score += 1000
                    elif duzina == uslov_pobede - 2:
                        # dva koraka do pobede
                        score += 500
                    else:
                        # bonus proporcionalan duzini
                        score += duzina * 100

        return score

    # broji ostrva koja imaju bar jedan kamencic uz sebe
    @staticmethod
    def _broji_aktivna_ostrva(tabla, boja):
        count = 0
        for o in tabla.ostrva:
            if o.boja != boja:
                continue
            for s_idx in o.susedi:
                if tabla.raspored_polja[s_idx].boja == boja:
                    count += 1
                    break
        return count

    # proverava da li postoji put izmedju dva ostrva (bez side-effecta)
    # trenutno duplikat tabla.postoji_put ali moram da sredim ponistavanje povezivanje ostrva....
    @staticmethod
    def _postoji_put_izmedju(tabla, o1, o2):
        from collections import deque

        # provera da l su ostrva povezana
        o1_aktivno = any(tabla.raspored_polja[s].boja == o1.boja for s in o1.susedi)
        o2_aktivno = any(tabla.raspored_polja[s].boja == o2.boja for s in o2.susedi)

        if not o1_aktivno or not o2_aktivno or o1.boja != o2.boja:
            return False

        queue = deque()
        visited = set()

        # dodaj susede prvog ostrva koji su iste boje
        for s in o1.susedi:
            if tabla.raspored_polja[s].boja == o1.boja:
                queue.append(s)

        while queue:
            idx = queue.popleft()
            if idx in visited:
                continue
            visited.add(idx)

            polje = tabla.raspored_polja[idx]
            if polje.boja != o1.boja:
                continue

            # da li smo stigli do drugog ostrva
            if idx in o2.susedi:
                return True

            for s in polje.susedi:
                if s not in visited:
                    queue.append(s)

        return False

