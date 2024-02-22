import os
import re
from collections import defaultdict
from collections.abc import Sequence
from typing import Literal, Mapping

from spectrumlab_line_database.filter import Filter, RE_ELEMENT_EN, RE_ELEMENT_RU
from spectrumlab_line_database.filter import WAVELENGTH_PATTERN, KIND_PATTERN, IONIZATION_DEGREE_PATTERN
from spectrumlab_line_database.sorter import Sorter

from spectrumlab.typing import NanoMeter, Symbol


DATABASE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')
DATABASE_KIND = 'atom'
DATABASE_VERSION = '4'


class Database(dict):

    def __init__(self, filter: Filter | None = None, sorter: Sorter | None = None, kind: str = DATABASE_KIND, version: str = DATABASE_VERSION, filedir: str = DATABASE_DIRECTORY):
        self._filter = filter or Filter()
        self._sorter = sorter or Sorter.none
        self._version = version
        self._kind = kind
        self._filedir = filedir

        self._data = self._parse_data()

    @property
    def version(self) -> str:
        return self._version

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def filedir(self) -> str:
        return self._filedir

    @property
    def filepath(self) -> str:
        return os.path.join(self.filedir, f'{self.kind} v{self.version}.mnd')

    @property
    def filter(self) -> Filter:
        return self._filter

    @property
    def sorter(self) -> Sorter:
        return self._sorter

    @property
    def data(self) -> Mapping[Symbol, Sequence[NanoMeter]]:
        return self._data

    def keys(self) -> Sequence[Symbol]:
        return self.data.keys()

    # --------            private            --------
    def _parse_data(self) -> Mapping[Symbol, Sequence[NanoMeter]]:
        filter = self.filter
        re_line = self.filter.pattern

        element = None

        data = defaultdict(list)
        with open(self.filepath, encoding='utf-8') as file:
            for line in file.readlines():
                line = line.strip()

                # element
                if re.match(RE_ELEMENT_EN, line) or re.match(RE_ELEMENT_RU, line):
                    element = line.split()[1]

                if filter.elements:
                    if (filter.elements.kind == 'only') and (element not in filter.elements):
                        continue
                    if (filter.elements.kind == 'only not') and (element in filter.elements):
                        continue

                # wavelength
                if element and re.match(re_line, line):
                    wavelength = float(re.search(WAVELENGTH_PATTERN, line)[0])

                    if filter.wavelength_span:
                        lb, ub = filter.wavelength_span
                        if (wavelength < lb) or (wavelength > ub):
                            continue

                    if filter.kind:
                        kind = re.search(KIND_PATTERN, line)[0][1:]
                        if isinstance(filter.kind, str):
                            if filter.kind not in kind:
                                continue
                        if isinstance(filter.kind, Sequence):
                            if any(item not in kind for item in filter.kind):
                                continue

                    if filter.ionization_degree_max:
                        ionization_degree_max = int(re.search(IONIZATION_DEGREE_PATTERN, line)[0][2:])
                        if ionization_degree_max > filter.ionization_degree_max:
                            continue

                    if filter.intensity:
                        intensity = None
                        for pattern in filter.intensity.patterns:
                            if re.search(pattern, line):
                                intensity = float(re.search(pattern, line)[0][2:])
                                break

                        if intensity is None:
                            continue
                        if filter.intensity.intensity_min and (intensity < filter.intensity.intensity_min):
                            continue
                        if filter.intensity.intensity_max and (intensity > filter.intensity.intensity_max):
                            continue

                    data[element].append(wavelength)
                

        return data

    def __getitem__(self, key: Symbol) -> Sequence[NanoMeter]:
        sorter = self.sorter

        if sorter == Sorter.none:
            return self.data[key]
        if sorter == Sorter.wavelength:
            return sorted(self.data[key])

        raise ValueError(f'Sorter {sorter} is not supported yet!')

    def __len__(self) -> int:
        return sum(
            len(wavelength)
            for element, wavelength in self.data.items()
        )

    def __repr__(self) -> str:
        cls = self.__class__

        return f'{cls}({self.kind} v{self.version})'

    def __str__(self) -> str:
        return '\n'.join([
            '{element}: ({wavelength})'.format(
                element=element,
                wavelength='; '.join(map(str, self[element])),
            )
            for element in self.keys()
        ])
