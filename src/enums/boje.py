from enum import Enum


class Boje(Enum):
    CRNA = (0, 0, 0)
    BELA = (255, 255, 255)
    SVETLOSIVA = (210, 210, 210)
    TAMNOSIVA = (35, 35, 35)
    SIVA_POZADINA = (30, 30, 40)
    BEZ = (220, 200, 160)  # Bež boja
    BEZ_TAMNA = (200, 180, 140)  # Tamnija bež boja

    def __eq__(self, other):
        return self.value == other.value
