#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

from typing import List, Tuple

from tictactoe_algorithm import TicTacToeAlgorithm


class MinimaxAlgorithm(TicTacToeAlgorithm):

	def __init__(self, max_depth: int):
		self.max_depth = max_depth

	def get_algo_name(self):
		return "minimax"

	def __partial_heuristic_evaulation(self, count: int) -> int:
		'''
			Returns a weight for a number of X'es or O's.
			If there are 3 the same characters in a line (horizontal, vertical or across),
			then give it a weight of 100. 2 characters -> 10, 1 character -> 1.
		'''
		if count == 3:
			return 100
		if count == 2:
			return 10
		return 1

	def __heuristic_evaulation(self, board: List[List[int]]) -> int:
		'''
			Returns value/weight of a board.

			for each of 8 lines:
				±100 for line of three
				±10 for line of two
				±1 for one in a line
			+ for player_1
			- for player_2
		'''
		total = 0
		for player in range(1,3):
			value = 0
			for i in range(3):
				'''	xxx
					...
					...	'''
				count = 0
				if board[i][0] == player:
					count += 1
				if board[i][1] == player:
					count += 1
				if board[i][2] == player:
					count += 1
				value += self.__partial_heuristic_evaulation(count)
				'''	x..
					x..
					x..	'''
				count = 0
				if board[0][i] == player:
					count += 1
				if board[1][i] == player:
					count += 1
				if board[2][i] == player:
					count += 1
				value += self.__partial_heuristic_evaulation(count)

			'''	x..
				.x.
				..x	'''
			count = 0
			if board[0][0] == player:
				count += 1
			if board[1][1] == player:
				count += 1
			if board[2][2] == player:
				count += 1
			value += self.__partial_heuristic_evaulation(count)

			'''	..x
				.x.
				x..	'''
			count = 0
			if board[0][2] == player:
				count += 1
			if board[1][1] == player:
				count += 1
			if board[2][0] == player:
				count += 1
			value += self.__partial_heuristic_evaulation(count)

			if player == 2:
				value *= -1
			total += value
		return total

	def __calculate_best(self, index: int, moves_before: int, max_depth: int, depth: int = 0) -> int:
		''' Recursive function for minimax.'''
		board = super()._index_to_board(index)
		board_value = self.__heuristic_evaulation(board)
		who_won = super().who_won(board)
		if who_won == 0 and depth <= max_depth:  # if no one won, depth isn't too high and there are possible moves left
			current_player = (moves_before + depth + 1) % 2 + 1
			other_player = current_player % 2 + 1
			best_value = None
			best_index = None
			next_moves = super()._get_all_next_moves(index, current_player)
			for index2 in next_moves:
				index3, value2 = self.__calculate_best(index2, moves_before, max_depth, depth + 1)
				if current_player == 2:  # if it is the opponent's turn, then minimise it instead of maximizing
					value2 *= -1
				# if current next move is better, then save it
				if best_index is None or value2 > best_value:
					best_value = value2
					best_index = index2
			return best_index, best_value
		return None, board_value

	def get_next_move(self, board: List[List[int]]) -> Tuple[int, int]:
		''' Returns a best move calculated by the minimax algorithm. '''
		current_board_index = super()._board_to_index(board)
		moves_before = 9 - super().num_of_available_spots(board)
		next_index, best_value = self.__calculate_best(current_board_index, moves_before, self.max_depth)
		difference = next_index - current_board_index
		for y in range(3):
			for x in range(3):
				if difference == 1 or difference >> 1 == 1:
					return (x, y)
				difference >>= 2  # bitwise operations for optimization
