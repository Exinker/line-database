import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal, get_args

from spectrumlab.typing import NanoMeter, Symbol


Ionization = Literal[1, 2, 3]


RE_ELEMENT_RU = re.compile(r' {1,}'.join([
    r'[0-9]{1,3}',  # atomic_number
    r'[A-Z]{1,1}[a-z]{0,2}',  # symbol
    r'[A-Я]{1,1}[а-я]*',  # name
    r'[0-9]{1,}.[0-9]{1,}',  # atomic_weight
]))
RE_ELEMENT_EN = re.compile(r' {1,}'.join([
    r'[0-9]{1,3}',  # atomic_number
    r'[A-Z]{1,1}[a-z]{0,2}',  # symbol
    r'[A-Z]{1,1}[a-z]*',  # name
    r'[0-9]{1,}.[0-9]{1,}',  # atomic_weight
]))

WAVELENGTH_PATTERN = r'^[0-9]{1,}.[0-9]{1,}'
KIND_PATTERN = '/[A, C, S, K, R, N, G]*'
IONIZATION_DEGREE_PATTERN = 'O=[{values}]{{1,1}}'.format(
    values=','.join(map(str, get_args(Ionization))),
)
INTENSITY_PATTERN = 'I=[0-9]{1,}'


@dataclass
class FilterElements:
    elements: Sequence[Symbol]
    kind: Literal['only', 'only not'] = field(default='only')

    # --------        private        --------
    def __contains__(self, symbol: Symbol) -> bool:
        return symbol in self.elements


@dataclass
class Filter:
    kind: str | Sequence[str] | None = field(default=None)
    ionization_degree_max: Ionization | None = field(default=1)
    intensity_min: float | None = field(default=None)
    wavelength_span: tuple[NanoMeter, NanoMeter] | None = field(default=None)
    elements: FilterElements | None = field(default=None)

    @property
    def pattern(self) -> str:

        items = []
        items.append(WAVELENGTH_PATTERN)
        if self.kind is not None:
            items.append(KIND_PATTERN)
        if self.ionization_degree_max is not None:
            items.append(IONIZATION_DEGREE_PATTERN)
        if self.intensity_min is not None:
            items.append(INTENSITY_PATTERN)

        return re.compile(r' {1,}'.join(items))
