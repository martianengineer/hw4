#!/usr/bin/env python3

import json
import keyword
from typing import Any, Dict, List


class Bunch:
    _SIMPLE_TYPES = (bool, int, float, str)

    @staticmethod
    def _parse_item(item):
        if isinstance(item, Bunch._SIMPLE_TYPES):
            return item
        elif isinstance(item, list):
            return Bunch._parse_list(item)
        elif isinstance(item, dict):
            return Bunch(item)
        else:
            raise ValueError("item is of unsupported type")

    @staticmethod
    def _parse_list(items: List) -> List:
        return [Bunch._parse_item(item) for item in items]

    def __init__(self, dictionary: Dict[str, Any]):
        for key, value in dictionary.items():
            if not isinstance(key, str):
                raise ValueError("key is not of string type")
            if keyword.iskeyword(key):
                key += '_'
            if key == 'price':
                key = '_price'
            setattr(self, key, Bunch._parse_item(value))


class ColorizeMixin:
    # Default color (yellow).
    color_code = 33

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs);

    def colorize(self, string: str) -> str:
        return f'\033[{self.color_code}m{string}\033[0m'


class Advert(ColorizeMixin, Bunch):
    def __init__(self, dictionary: Dict[str, Any]):
        super().__init__(dictionary)

        if not hasattr(self, 'title'):
            raise ValueError("title is missing")

        if hasattr(self, '_price'):
            if not isinstance(self._price, (int, float)):
                raise ValueError(f"{self._price} is of unsupported type")
            if self._price < 0:
                raise ValueError("price must be nonnegative")
        else:
            self._price = 0

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price must be nonnegative")
        self._price = value

    def __repr__(self) -> str:
        return self.colorize(f'{self.title} | {self.price} ₽')


CORGI_JSON_STR = """
{
  "title": "Вельш-корги",
  "price": 1000,
  "class": "dogs",
  "location": {
    "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
  }
}"""

IPHONE_JSON_STR = """
{
  "title": "iPhone X",
  "price": 100,
  "location": {
    "address": "город Самара, улица Мориса Тореза, 50",
    "metro_stations": ["Спортивная", "Гагаринская"]
  }
}
"""

INVALID_PYTHON_JSON_STR = """ 
{
    "title": "python", 
    "price": -1
}"""


def main():
    corgi_ad = Advert(json.loads(CORGI_JSON_STR))
    print(corgi_ad)
    print(corgi_ad.class_)

    iphone_ad = Advert(json.loads(IPHONE_JSON_STR))
    # Red.
    iphone_ad.color_code = 31
    print(iphone_ad)
    print(iphone_ad.location.address)
    print(iphone_ad.location.metro_stations)

    try:
        python_ad = Advert(json.loads(INVALID_PYTHON_JSON_STR))
    except Exception as e:
        print(f"Failed to create ad: {e}")

    try:
        iphone_ad.price = -10
    except Exception as e:
        print(f"Failed to set price: {e}")


if __name__ == '__main__':
    main()
