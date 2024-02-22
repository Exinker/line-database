# Line Database

Парсер базы данных спектральных линий [ПО Атом](https://www.vmk.ru/product/programmnoe_obespechenie/atom.html). 


## Author Information:
Павел Ващенко (vaschenko@vmk.ru)
[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2024 г.


## Installation
### Установка Python
Для работы требуется установить Python версии 3.10. *Ссылку на последнюю версию можно скачать [здесь](https://www.python.org/downloads/).*

### Установка виртуального окружения
Зависимости, необходимые для работы приложения, необходимо установить в виртуальное окружение `env`. Для этого в командной строке необходимо:
1. Зайди в папку с приложением: `cd PATH`, где `PATH` - путь до директории;
2. Создать виртуальное окружение: `python -m venv env`;
3. Активировать виртуальное окружение: `env\Scripts\activate.bat`;
4. Установить зависимости в виртуальное окружение: `pip install -r requirements.txt`;


## Usage
Пример использования библиотеки:
```python
from spectrumlab_line_database import Database, Filter, FilterElements, Sorter


if __name__ == '__main__':
    elements = ['Cu']

    database = Database(
        filter=Filter(
            kind='A',
            ionization_degree_max=1,
            intensity=FilterIntensity(
                key='I',
                intensity_min=2500,
            ),
            wavelength_span=[120, 900],
            elements=FilterElements(elements, kind='only'),
        ),
        sorter=Sorter.wavelength,
    )

    print(database)  # Cu: (261.8365; 296.1165; 324.7532; 327.3954)

```