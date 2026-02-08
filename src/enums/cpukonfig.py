from enum import Enum


# tipovi unosa u transpozicionoj tabeli
class CpuKonfig(Enum):
    TT_TACAN = 0  # tacna vrednost
    TT_DONJA_GRANICA = 1  # beta odsecanje
    TT_GORNJA_GRANICA = 2  # alpha odsecanje
    DUBINA = 20
    DEBUG = True
    CVOROVI_ZA_POZIV_VREMENA = 4096
