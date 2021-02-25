#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

import pickle
from typing import List, Tuple

from tictactoe_algorithm import TicTacToeAlgorithm


class BruteforceAlgorithm(TicTacToeAlgorithm):

	tree = [None] * (2 ** 18)  # reserve memory for all combinations and assign None
	# tree[n] = <int> if the best move is <int>

	def __init__(self, save = 0, load = 0):
		if load:
			with open('bruteforce.pickle', 'rb') as f:
				self.tree = pickle.load(f)
		else:
			self.__calculate_best()
			if save:
				with open('bruteforce.pickle', 'wb') as f:
					pickle.dump(self.tree, f)

	def get_algo_name(self):
		return "bruteforce"

	def __calculate_best(self, index: int = 0, depth: int = 0) -> Tuple[int, int]:
		''' Recursive function for filling the "tree" array.'''
		board = super()._index_to_board(index)
		who_won = super().who_won(board)
		if who_won == 0:  # if no one won, then check all next possible moves

			current_player = depth % 2 + 1
			other_player = current_player % 2 + 1
			best_who_won = None
			best_depth = 10  # depth is never greater than 9
			best_index = None

			next_moves = super()._get_all_next_moves(index, current_player)
			for index2 in next_moves:
				depth2, who_won2 = self.__calculate_best(index2, depth + 1)

				# if current next move is better, then save it
				if (best_index is None or
					(best_who_won == other_player and (who_won2 == 3 or who_won2 == current_player)) or
					(best_who_won == 3 and who_won2 == current_player)):
					best_who_won = who_won2
					best_depth = depth2
					best_index = index2
				elif best_who_won == who_won2 and depth2 < best_depth:  # current next move has the same winning player, but has smaller depth
					best_depth = depth2
					best_index = index2

			self.tree[index] = best_index  # save the best move
			return (best_depth, best_who_won)
		return (depth, who_won)

	def get_next_move(self, board: List[List[int]]) -> Tuple[int, int]:
		''' Returns a best move fetched from "tree" array. '''
		current_board_index = super()._board_to_index(board)
		next_index = self.tree[current_board_index]
		difference = next_index - current_board_index
		for y in range(3):
			for x in range(3):
				if difference == 1 or difference >> 1 == 1:
					return (x, y)
				difference >>= 2  # bitwise operations for optimization
