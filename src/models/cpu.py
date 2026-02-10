import time
from collections import deque

from src.enums.cpukonfig import CpuKonfig
from src.models.unionfind import UnionFind
from src.models.tabla import Tabla
from src.enums.boje import Boje


class Cpu:
    # pretraga, u sekundama
    # pretraga, u sekundama

    # transpoziciona tabela koja koristi
    # zobrist hash (dubina, vrednost, tip, najbolji_potez)
    __transpoziciona_tabela = {}

    # potezi koji su izazvali odsecanje na datoj dubini
    # za datu dubinu cuva [potez1, potez2]
    __killer_potezi = {}

    VREME_LIMIT = None  # pretraga, u sekundama

    # pracenje vremena i stanja pretrage
    __pocetak_pretrage = 0
    __prekinuta_pretraga = False
    __brojac_cvorova = 0

    # indeks najboljeg poteza i njegova vrednost
    # koristi iterativno produbljivanje, to jest pretrazuje od dubine 1 nagore
    # rezultati plice pretrage pomazu u sortiranju poteza za dublju

    @staticmethod
    def postavi_vreme_trazenja(n):
        Cpu.VREME_LIMIT = 2 * n

    @staticmethod
    def najbolji_potez(tabla, cpu_boja):
        # ponovo racunamo hash pre pretrage jer su pravi potezi menjali tablu
        tabla.izracunaj_zobrist_hash()
        Cpu.__killer_potezi.clear()
        Cpu.__pocetak_pretrage = time.time()

        best_potez = None
        best_vrednost = float("-inf")

        # iterativno produbljivanje od dubine 1 do maksimalne
        for d in range(1, CpuKonfig.DUBINA.value + 1):
            Cpu.__prekinuta_pretraga = False
            Cpu.__brojac_cvorova = 0

            vrednost, potez = Cpu.minimax(tabla, d, True, cpu_boja, float("-inf"), float("inf"))

            # ako je pretraga prekinuta zbog vremena, ne koristimo rezultat
            if Cpu.__prekinuta_pretraga:
                if CpuKonfig.DEBUG:
                    proteklo = time.time() - Cpu.__pocetak_pretrage
                    print(f"[CPU] Dubina {d}: prekinuto (vreme = {proteklo:.2f}s)")
                break

            if potez is not None:
                best_potez = potez
                best_vrednost = vrednost

            if CpuKonfig.DEBUG:
                polje = tabla.raspored_polja[potez] if potez is not None else None
                proteklo = time.time() - Cpu.__pocetak_pretrage
                if polje:
                    print(f"[CPU] Dubina {d}: {polje.slovo}{polje.broj} "
                          f"(vrednost = {vrednost}, vreme = {proteklo:.2f}s, "
                          f"cvorova = {Cpu.__brojac_cvorova}, TT = {len(Cpu.__transpoziciona_tabela)})")

            # ako smo nasli sigurnu pobedu ili poraz, nema potrebe za daljom pretragom
            if abs(best_vrednost) >= 10000:
                break

            # procena da li ima vremena za sledecu dubinu
            # sledeca dubina traje otprilike branching_factor puta duze
            proteklo = time.time() - Cpu.__pocetak_pretrage
            if proteklo > Cpu.VREME_LIMIT:
                break

        if CpuKonfig.DEBUG and best_potez is not None:
            polje = tabla.raspored_polja[best_potez]
            ukupno = time.time() - Cpu.__pocetak_pretrage
            print(f"[CPU] Najbolji potez: {polje.slovo}{polje.broj} "
                  f"(vrednost = {best_vrednost}, ukupno = {ukupno:.2f}s)")

        return best_potez

    # minimax sa alfa beta odsecanjem, transpozicionom tabelom,
    # redukcijom prostora pretrage, sortiranjem poteza i killer heuristikom
    @staticmethod
    def minimax(tabla, dubina, maksimizuje, cpu_boja, alpha, beta):
        # provera vremenskog limita svakih 4096 cvorova
        Cpu.__brojac_cvorova += 1
        if Cpu.__brojac_cvorova % CpuKonfig.CVOROVI_ZA_POZIV_VREMENA.value == 0:
            if time.time() - Cpu.__pocetak_pretrage > Cpu.VREME_LIMIT:
                Cpu.__prekinuta_pretraga = True
                return 0, None

        # pocetne vrednosti alpha i beta za odredjivanje tipa unosa u tt
        pocetni_alpha = alpha
        pocetni_beta = beta

        protivnik_boja = Boje.CRNA if cpu_boja == Boje.BELA else Boje.BELA
        trenutna_boja = cpu_boja if maksimizuje else protivnik_boja

        # provera transpozicione tabele pre pretrage
        tt_hash = tabla.zobrist_hash
        tt_potez = None
        tt_unos = Cpu.__transpoziciona_tabela.get(tt_hash)
        if tt_unos is not None:
            tt_dubina, tt_vrednost, tt_tip, tt_potez = tt_unos
            # samo ako je iz pretrage >= dubine
            if tt_dubina >= dubina:
                if tt_tip == CpuKonfig.TT_TACAN:
                    return tt_vrednost, tt_potez
                elif tt_tip == CpuKonfig.TT_DONJA_GRANICA:
                    alpha = max(alpha, tt_vrednost)
                elif tt_tip == CpuKonfig.TT_GORNJA_GRANICA:
                    beta = min(beta, tt_vrednost)

                if alpha >= beta:
                    return tt_vrednost, tt_potez

        moguci_potezi = tabla.relevantni_potezi()
        if not moguci_potezi:
            moguci_potezi = Tabla.svi_moguci_potezi(tabla.bit_vector(False))

        # izlazak iz rekurzije
        if dubina == 0 or not moguci_potezi:
            vrednost = Cpu.heuristika(tabla, cpu_boja)
            Cpu.__transpoziciona_tabela[tt_hash] = (0, vrednost, CpuKonfig.TT_TACAN, None)
            return vrednost, None

        moguci_potezi = Cpu.__sortiraj_poteze(tabla, moguci_potezi, trenutna_boja, dubina, tt_potez)
        najbolji_potez = moguci_potezi[0]

        # maksimizujuci deo minimaxa
        if maksimizuje:
            max_vrednost = float("-inf")
            for potez_idx in moguci_potezi:
                # simulacija odigravanja poteza, ali bez propratnih efekata
                tabla.primeni_potez_simulacija(potez_idx, trenutna_boja)

                # provera pobede simuliranog poteza
                if tabla.provera_pobede_simulacija(trenutna_boja):
                    tabla.ponisti_potez(potez_idx, trenutna_boja)

                    # pobednicki potez u transpozicionu tabelu
                    Cpu.__transpoziciona_tabela[tt_hash] = (dubina, 10000, CpuKonfig.TT_TACAN, potez_idx)
                    return 10000, potez_idx

                vrednost, _ = Cpu.minimax(tabla, dubina - 1, False, cpu_boja, alpha, beta)

                # ponistavanje simuliranog poteza
                tabla.ponisti_potez(potez_idx, trenutna_boja)

                # ako je pretraga prekinuta, vracamo se odmah
                if Cpu.__prekinuta_pretraga:
                    return 0, None

                if vrednost > max_vrednost:
                    max_vrednost = vrednost
                    najbolji_potez = potez_idx

                # alfa odsecanje
                alpha = max(alpha, vrednost)
                if beta <= alpha:
                    # potez koji je izazvao odsecanje
                    Cpu.__dodaj_killer_potez(dubina, potez_idx)
                    break

            if max_vrednost == float("-inf"):
                return 0, najbolji_potez

            # odredjivanje tipa unosa za transpozicionu tabelu
            if max_vrednost <= pocetni_alpha:
                tt_tip = CpuKonfig.TT_GORNJA_GRANICA
            elif max_vrednost >= pocetni_beta:
                tt_tip = CpuKonfig.TT_DONJA_GRANICA
            else:
                tt_tip = CpuKonfig.TT_TACAN
            Cpu.__transpoziciona_tabela[tt_hash] = (dubina, max_vrednost, tt_tip, najbolji_potez)

            return max_vrednost, najbolji_potez

        # minimizujuci deo minimaxa, komentari su relativno
        # ekvivalentni maksimizujucem
        else:
            min_vrednost = float("inf")
            for potez_idx in moguci_potezi:
                tabla.primeni_potez_simulacija(potez_idx, trenutna_boja)

                if tabla.provera_pobede_simulacija(trenutna_boja):
                    tabla.ponisti_potez(potez_idx, trenutna_boja)
                    Cpu.__transpoziciona_tabela[tt_hash] = (dubina, -10000, CpuKonfig.TT_TACAN, potez_idx)
                    return -10000, potez_idx

                vrednost, _ = Cpu.minimax(tabla, dubina - 1, True, cpu_boja, alpha, beta)

                tabla.ponisti_potez(potez_idx, trenutna_boja)

                if Cpu.__prekinuta_pretraga:
                    return 0, None

                if vrednost < min_vrednost:
                    min_vrednost = vrednost
                    najbolji_potez = potez_idx

                beta = min(beta, vrednost)
                if alpha >= beta:
                    # potez koji je izazvao odsecanje
                    Cpu.__dodaj_killer_potez(dubina, potez_idx)
                    break

            if min_vrednost == float("inf"):
                return 0, najbolji_potez

            if min_vrednost <= pocetni_alpha:
                tt_tip = CpuKonfig.TT_GORNJA_GRANICA
            elif min_vrednost >= pocetni_beta:
                tt_tip = CpuKonfig.TT_DONJA_GRANICA
            else:
                tt_tip = CpuKonfig.TT_TACAN
            Cpu.__transpoziciona_tabela[tt_hash] = (dubina, min_vrednost, tt_tip, najbolji_potez)

            return min_vrednost, najbolji_potez

    # brza procena kvaliteta poteza za sortiranje
    # visok skor znaci da je potez verovatno dobar
    # koristi se za sortiranje poteza za bolji alfa beta pruning
    @staticmethod
    def __oceni_potez(tabla, potez_idx, boja):
        score = 0
        polje = tabla.raspored_polja[potez_idx]
        protivnik_boja = Boje.CRNA if boja == Boje.BELA else Boje.BELA

        for s in polje.susedi:
            sused_boja = tabla.raspored_polja[s].boja
            # pridodaje veci znacaj sirenju sopstvenog lanca
            if sused_boja == boja:
                score += 3
            elif sused_boja == protivnik_boja:
                score += 1

        # jos veci znacaj ako potez aktivira neko ostrvo
        for o in tabla.ostrva:
            if o.boja == boja and potez_idx in o.susedi:
                score += 5
                break

        return score

    # sortira poteze za bolje alfa-beta odsecanje
    # redosled prioriteta
    # TT potez > killer potezi > procenjen skor
    @staticmethod
    def __sortiraj_poteze(tabla, potezi, boja, dubina, tt_potez):
        killeri = Cpu.__killer_potezi.get(dubina, [])

        # nije mogla lambda </3
        def kljuc(idx):
            if idx == tt_potez:
                return 10000
            if idx in killeri:
                return 5000
            return Cpu.__oceni_potez(tabla, idx, boja)

        potezi.sort(key=kljuc, reverse=True)
        return potezi

    # dodaje potez u listu killer poteza za datu dubinu
    # cuva se maksimalno 2 killer poteza po dubini
    @staticmethod
    def __dodaj_killer_potez(dubina, potez_idx):
        if dubina not in Cpu.__killer_potezi:
            Cpu.__killer_potezi[dubina] = []
        killeri = Cpu.__killer_potezi[dubina]
        if potez_idx not in killeri:
            killeri.insert(0, potez_idx)
            if len(killeri) > 2:
                killeri.pop()

    # procenjuje vrednost stanja
    @staticmethod
    def heuristika(tabla, cpu_boja):
        protivnik_boja = Boje.CRNA if cpu_boja == Boje.BELA else Boje.BELA

        cpu_a, cpu_k, cpu_d, cpu_p = Cpu.__evaluacija_pozicije(tabla, cpu_boja)
        prot_a, prot_k, prot_d, prot_p = Cpu.__evaluacija_pozicije(tabla, protivnik_boja)

        score = 0
        # aktivna ostrva
        score += (cpu_a - prot_a) * 50
        # kamencici uz ostrva
        score += (cpu_k - prot_k) * 25
        # duzina lanaca od ostrva
        score += (cpu_d - prot_d) * 20
        # spojeni parovi ostrva
        score += cpu_p - prot_p

        return score

    # objedinjena evaluacija za jednu boju
    # aktivna ostrva, kamencici uz ostrva, duzina lanaca i spojeni parovi
    # radi jednan bfs po aktivnom ostrvu i koristi union find za pracenje spojenih parova
    @staticmethod
    def __evaluacija_pozicije(tabla, boja):
        ostrva_boje = [(i, o) for i, o in enumerate(tabla.ostrva) if o.boja == boja]

        # mapa polje na listu indeksa ostrva kojima je to polje susedno
        # omogucava brzu proveru da li BFS stize do nekog ostrva
        polje_ostrva = {}
        for i, o in ostrva_boje:
            for s in o.susedi:
                polje_ostrva.setdefault(s, []).append(i)

        # disjoint set struktura za
        # union find operacije
        # https://www.geeksforgeeks.org/dsa/introduction-to-disjoint-set-data-structure-or-union-find-algorithm/
        parent = {oi: oi for oi, _ in ostrva_boje}
        uf = UnionFind(parent)

        aktivna = 0
        kamencici_uz_ostrva = 0
        ukupna_duzina = 0
        visited = set()

        # za svako poseceno polje pamtimo koje ostrvo ga je otkrilo
        # kad BFS naleti na vec poseceno polje, spajamo ta dva ostrva
        polje_vlasnik = {}

        for i, o in ostrva_boje:
            dodirujuca_polja = []
            for s in o.susedi:
                if tabla.raspored_polja[s].boja == boja:
                    dodirujuca_polja.append(s)
                    kamencici_uz_ostrva += 1

            if not dodirujuca_polja:
                continue
            aktivna += 1

            # ako su svi seeds vec poseceni, ovo ostrvo je vec u nekoj komponenti
            # samo ga spajamo sa vlasnikom tih polja
            for s in dodirujuca_polja:
                if s in polje_vlasnik:
                    uf.union(i, polje_vlasnik[s])

            # bfs od neposecenih seed-ova
            queue = deque()
            for s in dodirujuca_polja:
                if s not in visited:
                    queue.append(s)

            lokalni_visited = set()
            while queue:
                idx = queue.popleft()
                if idx in lokalni_visited:
                    continue

                if idx in visited:
                    if idx in polje_vlasnik:
                        uf.union(i, polje_vlasnik[idx])
                    continue

                lokalni_visited.add(idx)

                if tabla.raspored_polja[idx].boja != boja:
                    continue

                ukupna_duzina += 1
                polje_vlasnik[idx] = i

                if idx in polje_ostrva:
                    for oj in polje_ostrva[idx]:
                        uf.union(i, oj)

                for s in tabla.raspored_polja[idx].susedi:
                    if s not in lokalni_visited:
                        queue.append(s)

            visited.update(lokalni_visited)

        # grupisanje ostrva po komponentama sa union find
        komponente = {}
        for i, _ in ostrva_boje:
            root = uf.find(i)
            komponente.setdefault(root, set()).add(i)

        # evaluacija spojenih parova ostrva po komponentama
        score_parovi = 0
        for _, ostrva_set in komponente.items():
            if len(ostrva_set) < 2:
                continue
            ostrva_lista = sorted(ostrva_set)
            for i in range(len(ostrva_lista)):
                for j in range(i + 1, len(ostrva_lista)):
                    duzina = Tabla.duzina_obodnog_puta(ostrva_lista[i], ostrva_lista[j])
                    if duzina >= 7:
                        # pobeda
                        score_parovi += 5000
                    elif duzina == 6:
                        # jedan korak do pobede
                        score_parovi += 3000
                    elif duzina == 5:
                        # dva koraka do pobede
                        score_parovi += 1500
                    else:
                        # bonus proporcionalan duzini
                        score_parovi += duzina * 150

        return aktivna, kamencici_uz_ostrva, ukupna_duzina, score_parovi
