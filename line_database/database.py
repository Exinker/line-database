import os
import re
from collections import defaultdict
from collections.abc import Sequence
from typing import Mapping

from line_database.filter import Filter, RE_ELEMENT
from line_database.filter import WAVELENGTH_PATTERN, KIND_PATTERN, IONIZATION_DEGREE_PATTERN, INTENSITY_PATTERN
from line_database.sorter import Sorter
from line_database.typing import NanoMeter, Symbol


DATABASE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')
DATABASE_VERSION = '4'


class Database(dict):

    def __init__(self, filter: Filter | None = None, sorter: Sorter | None = None, order_max: int = 1, version: str = DATABASE_VERSION, filedir: str = DATABASE_DIRECTORY):
        self._filter = filter or Filter()
        self._sorter = sorter or Sorter.none
        self._order_max = order_max
        self._version = version
        self._filedir = filedir

        self._data = self._parse_data()

    @property
    def version(self) -> str:
        return self._version

    @property
    def filedir(self) -> str:
        return self._filedir

    @property
    def filepath(self) -> str:
        return os.path.join(self.filedir, f'atom v{self.version}.mnd')

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
    def _parse_data(self):
        filter = self.filter
        re_line = self.filter.pattern

        symbol = None

        db = defaultdict(list)
        with open(self.filepath, encoding='utf-8') as file:
            for i, line in enumerate(file.readlines()):
                line = line.strip()

                if re.match(RE_ELEMENT, line):
                    symbol = line.split()[1]

                if symbol and re.match(re_line, line):

                    # wavelength
                    wavelength = float(re.search(WAVELENGTH_PATTERN, line)[0])

                    # filter / kind
                    if filter.kind:
                        kind = re.search(KIND_PATTERN, line)[0][1:]
                        if isinstance(filter.kind, str):
                            if filter.kind not in kind:
                                continue
                        if isinstance(filter.kind, Sequence):
                            if any(item not in kind for item in filter.kind):
                                continue

                    # filter / ionization_degree_max
                    if filter.ionization_degree_max:
                        ionization_degree_max = int(re.search(IONIZATION_DEGREE_PATTERN, line)[0][2:])
                        if ionization_degree_max > filter.ionization_degree_max:
                            continue

                    # filter / intensity_min
                    if filter.intensity_min:
                        intensity = float(re.search(INTENSITY_PATTERN, line)[0][2:])
                        if intensity < filter.intensity_min:
                            continue

                    #
                    db[symbol].extend([
                        wavelength*n
                        for n in range(1, self._order_max + 1)
                    ])

        return db

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
            for symbol, wavelength in self.data.items()
        )

    def __repr__(self) -> str:
        cls = self.__class__

        return f'{cls}(v{self.version})'

    def __str__(self) -> str:
        return '\n'.join([
            '{symbol}: ({wavelength})'.format(
                symbol=symbol,
                wavelength='; '.join(map(str, wavelength))
            )
            for symbol, wavelength in self.data.items()
        ])
