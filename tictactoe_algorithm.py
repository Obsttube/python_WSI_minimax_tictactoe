#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

from abc import ABC, abstractmethod
from typing import List, Tuple


class TicTacToeAlgorithm(ABC):

	@abstractmethod
	def get_next_move(self, board: List[List[int]]) -> Tuple[int, int]:
		''' Returns (x, y) of the next move.'''
		pass

	@abstractmethod
	def get_algo_name(self):
		''' Returns name of the algorithm.'''
		pass

	@classmethod
	def who_won(cls, board: List[List[int]]) -> int:
		'''
			Returns 0 if no one won and there are still possible moves left,
			1 if player_1 won,
			2 if player_2 won,
			3 if it is a tie (no one won and there are no possible moves left)
		'''
		for player in range(1,3):
			for i in range(3):
				if ((board[i][0] == player and board[i][1] == player and board[i][2] == player) or  # horizontal line
					(board[0][i] == player and board[1][i] == player and board[2][i] == player)):  # vertical line
					return player
			if ((board[0][0] == player and board[1][1] == player and board[2][2] == player) or  # diagonal 1
				(board[2][0] == player and board[1][1] == player and board[0][2] == player)):  # diagonal 2
				return player
		for y in range(3):
			for x in range(3):
				if board[y][x] == 0:
					return 0
		return 3

	@classmethod
	def num_of_available_spots(cls, board: List[List[int]]) -> int:
		''' Returns number of available spots.'''
		available_spots = 0
		for y in range(3):
			for x in range(3):
				if board[y][x] == 0:
					available_spots += 1
		return available_spots

	@classmethod
	def _get_all_next_moves(cls, index: int, current_player: int) -> List[int]:
		''' Returns array with all possible next moves.'''
		moves = []
		for i in range(9):
			if (index & (1 << (i * 2))) or (index & (2 << (i * 2))):
				continue
			moves.append(index | (current_player << (i * 2)))
		return moves

	@classmethod
	def _board_to_index(self, board: List[List[int]]) -> int:
		''' Converts board array to int representation.'''
		index = 0
		value = 1  # upper left corner
		'''
			player_1 (my) values:
			------------------
			|  1 |  4  |  16 |
			| 32 | 256 |1024 |
			|4096|16384|65536|
			------------------
			player_2 (opponent) values:
			-------------------
			|  2 |  8  |  32  |
			|128 | 512 | 2048 |
			|8192|32768|131072|
			-------------------
		'''
		for y in range(3):
			for x in range(3):
				if board[y][x] == 1:
					index += value
				value <<= 1  # change to player_2 (opponent), bitwise operations for optimization
				if board[y][x] == 2:
					index += value
				value <<= 1  # change back to player_1 (me) and move to the next spot
		return index

	@classmethod
	def _index_to_board(self, index: int) -> List[List[int]]:
		''' Converts board int representation to array.'''
		board = [[0, 0, 0],
		         [0, 0, 0],
		         [0, 0, 0]]
		for y in range(3):
			for x in range(3):
				if index & 1:
					board[y][x] = 1
				index >>= 1  # bitwise operations for optimization
				if index & 1:
					board[y][x] = 2
				index >>= 1
		return board
