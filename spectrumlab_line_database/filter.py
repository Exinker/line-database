import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal, get_args

from spectrumlab.typing import NanoMeter, Symbol


Ionization = Literal[1, 2, 3]


SPACE_PATTERN = r' {1,}'
RE_ELEMENT_RU = re.compile(fr'{SPACE_PATTERN}'.join([
    r'\d{1,3}',  # atomic_number
    r'[A-Z]{1,1}[a-z]{0,2}',  # element
    r'[A-Я]{1,1}[а-я]*',  # name
    r'\d{1,}.\d{1,}',  # atomic_weight
]))
RE_ELEMENT_EN = re.compile(fr'{SPACE_PATTERN}'.join([
    r'\d{1,3}',  # atomic_number
    r'[A-Z]{1,1}[a-z]{0,2}',  # element
    r'[A-Z]{1,1}[a-z]*',  # name
    r'\d{1,}.\d{1,}',  # atomic_weight
]))

WAVELENGTH_PATTERN = r'^\d{1,}.\d{1,}'
KIND_PATTERN = '/[ACSKRNG]*'
IONIZATION_DEGREE_PATTERN = 'O=[{values}]{{1,1}}'.format(
    values=','.join(map(str, get_args(Ionization))),
)


@dataclass
class FilterElements:
    elements: Sequence[Symbol]
    kind: Literal['only', 'only not'] = field(default='only')

    # --------        private        --------
    def __contains__(self, element: Symbol) -> bool:
        return element in self.elements


@dataclass
class FilterIntensity:
    key: str = field(default='I')
    intensity_min: float | None = field(default=None)
    intensity_max: float | None = field(default=None)

    @property
    def patterns(self) -> Sequence[str]:
        return (
            fr'{self.key}=\d{{1,}}{SPACE_PATTERN}',
            fr'{self.key}=\d{{1,}}.\d{{1,}}{SPACE_PATTERN}',
            fr'{self.key}=\d{{1,}}e[+-]\d{{1,3}}{SPACE_PATTERN}',
            fr'{self.key}=\d{{1,}}.\d{{1,16}}e[+-]\d{{1,3}}{SPACE_PATTERN}',
        )

    # --------        private        --------
    def __contains__(self, element: Symbol) -> bool:
        return element in self.elements


@dataclass
class Filter:
    kind: str | Sequence[str] | None = field(default=None)
    ionization_degree_max: Ionization | None = field(default=1)
    intensity: FilterIntensity | None = field(default=None)
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

        return re.compile(fr'{SPACE_PATTERN}'.join(items))
