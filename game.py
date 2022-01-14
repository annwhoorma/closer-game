import os
from pathlib import Path
from enum import Enum
from random import randint

Q, R, A = 0, 1, 2

class Game:
    def __init__(self, path: Path):
        self._cards = {
            Q: ['Q/'+f for f in os.listdir(Path(path, 'Q'))],
            R: ['R/'+f for f in os.listdir(Path(path, 'R'))],
            A: ['A/'+f for f in os.listdir(Path(path, 'A'))]
        }
        self._game_len = len(self._cards[Q]) + len(self._cards[R]) + len(self._cards[A])
        self.__generate_order()

    def __generate_order(self):
        # hardcoded yay
        order = [Q, A, Q, Q, A, Q, Q, R, Q, Q, A]
        assert len(order) == self._game_len, 'probably the hardcoded order should be changed'
        self.deck = []

        for heap_num in order:
            # update deck and remove used card from the heap
            heap = self._cards[heap_num]
            card_number = randint(0, len(heap)-1)
            card = heap[card_number]
            self.deck.append(card)
            heap.remove(card)

    def get_deck(self):
        return self.deck