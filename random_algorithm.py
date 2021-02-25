#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

from random import randint
from typing import List, Tuple

from tictactoe_algorithm import TicTacToeAlgorithm


class RandomAlgorithm(TicTacToeAlgorithm):

	def get_next_move(self, board: List[List[int]]) -> Tuple[int, int]:
		''' Returns a possible random move.'''
		available_spots = super().num_of_available_spots(board)
		choosen_spot = randint(0, available_spots - 1)
		current_spot = 0
		for y in range(3):
			for x in range(3):
				if board[y][x] == 0:
					if current_spot == choosen_spot:
						return (x, y)
					current_spot += 1

	def get_algo_name(self):
		return "random"
