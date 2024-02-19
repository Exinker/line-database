import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal, get_args


Ionization = Literal[1, 2, 3]


RE_ELEMENT = re.compile(r' {1,}'.join([
    r'^[0-9]{1,3}',  # atomic_number
    r'[A-Z][a-z]',  # symbol
    r'[A-Я][а-я]*',  # name
    r'[0-9]{1,}.[0-9]{1,}',  # atomic_weight
]))

WAVELENGTH_PATTERN = r'^[0-9]{1,}.[0-9]{1,}'
KIND_PATTERN = '/[A, C, S, K, R, N, G]*'
IONIZATION_PATTERN = 'O=[{values}]{{1,1}}'.format(
    values=','.join(map(str, get_args(Ionization))),
)
INTENSITY_PATTERN = 'I=[0-9]{1,}'


@dataclass
class Filter:
    kind: str | Sequence[str] | None = field(default=None)
    ionization_max: Ionization | None = field(default=1)
    intensity_min: float | None = field(default=None)

    @property
    def pattern(self) -> str:

        items = []
        items.append(WAVELENGTH_PATTERN)
        if self.kind is not None:
            items.append(KIND_PATTERN)
        if self.ionization_max is not None:
            items.append(IONIZATION_PATTERN)
        if self.intensity_min is not None:
            items.append(INTENSITY_PATTERN)

        return re.compile(r' {1,}'.join(items))
