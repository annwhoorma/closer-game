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

    def __rules_apply(self, heap_num, last_taken_from):
        '''doesnt depend on last_take_from for now
        '''
        is_heap_empty = len(self._cards[heap_num]) == 0
        return is_heap_empty

    def __generate_order(self):
        # can be deleted later if still not used
        last_taken_from = [None, None]
        num_heaps = len(self._cards.keys())
        self.deck = []

        for _ in range(self._game_len):
            # choose from which heap to draw
            if last_taken_from[-1] is None:
                heap_num = Q
            else:
                heap_num = randint(0, num_heaps-1)
                while self.__rules_apply(heap_num, last_taken_from):
                    heap_num = randint(0, num_heaps-1)
            # shift
            last_taken_from[0] = last_taken_from[-1]
            last_taken_from[-1] = heap_num
            # update deck and remove used card from the heap
            heap = self._cards[heap_num]
            card_number = randint(0, len(heap)-1)
            card = heap[card_number]
            self.deck.append(card)
            heap.remove(card)

    def get_deck(self):
        return self.deck