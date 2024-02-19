# Line Database

Парсер базы данных спектральных линий [ПО Атом](https://www.vmk.ru/product/programmnoe_obespechenie/atom.html). 


## Author Information:
Павел Ващенко (vaschenko@vmk.ru)
[ВМК-Оптоэлектроника](https://www.vmk.ru/), г. Новосибирск 2024 г.


## Installation
### Установка Python
Для работы требуется установить Python версии 3.10. *Ссылку на последнюю версию можно скачать [здесь](https://www.python.org/downloads/).*


## Usage
Пример использования библиотеки:
```python
from line_database import Database, Filter, Sorter


database = Database(
    filter=Filter(
        kind='ACSKG',
        ionization_max=1,
    ),
    sorter=Sorter.wavelength,
    order_max=2,
)

if __name__ == '__main__':
    element = 'Cu'

    content = '{element}: {items}.'.format(
        element=element,
        items=', '.join([f'{item:.4f}' for item in database['Cu']]),
    )
    print(content)  # Cu: 324.7532, 327.3954, 649.5064, 654.7908.

```