#!/usr/bin/env python3

import random
from abc import ABC, abstractmethod


class AnimeMon(ABC):
    @abstractmethod
    def inc_exp(self):
        pass

    @property
    @abstractmethod
    def exp(self):
        pass


class Pokemon(AnimeMon):
    def __init__(self, name: str):
        self.name = name
        self._exp = 0

    def inc_exp(self, value: int):
        self._exp += value

    @property
    def exp(self):
        return self._exp


class Digimon(AnimeMon):
    def __init__(self, name: str):
        self.name = name
        self._exp = 0

    def inc_exp(self, value: int):
        self._exp += 8 * value

    @property
    def exp(self):
        return self._exp


def train(pokemon: AnimeMon):
    step_size, level_size = 10, 100
    sparring_qty = (level_size - pokemon.exp % level_size) // step_size
    for _ in range(sparring_qty):
        win = random.choice([True, False])
        if win:
            pokemon.inc_exp(step_size)


def main():
    bulba = Pokemon(name='Bulbasaur')
    train(bulba)
    print(bulba.exp)

    digi = Digimon(name='Agumon')
    train(digi)
    print(digi.exp)


if __name__ == '__main__':
    main()
