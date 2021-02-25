#!/usr/bin/env python

__copyright__ = "Copyright 2020, Piotr Obst"

from random import randint
from timeit import default_timer as timer
from typing import List, Tuple

from tictactoe_algorithm import TicTacToeAlgorithm
from random_algorithm import RandomAlgorithm
from bruteforce_algorithm import BruteforceAlgorithm
from minimax_algorithm import MinimaxAlgorithm


def do_next_move(board: List[List[int]], player: int, algorithms: List[TicTacToeAlgorithm]) -> float:  # player = 1 or 2
    ''' Perform a next move.'''
    start = timer()
    x, y = algorithms[player - 1].get_next_move(board)
    end = timer()
    board[y][x] = player
    return end - start


def play(board: List[List[int]], algorithms_input: List[TicTacToeAlgorithm],  change_places: bool) -> Tuple[int, List[float]]:
    ''' Play a full game till the end.'''
    algorithms = [None, None]
    if change_places:
        algorithms[1] = algorithms_input[0]
        algorithms[0] = algorithms_input[1]
    else:
        algorithms[0] = algorithms_input[0]
        algorithms[1] = algorithms_input[1]
    player = 1
    times = [0.0, 0.0]
    while TicTacToeAlgorithm.who_won(board) == 0:
        time = do_next_move(board, player, algorithms)
        times[player - 1] += time
        player = player % 2 + 1
    who_won = TicTacToeAlgorithm.who_won(board)
    if change_places:
        tmp = times[1]
        times[1] = times[0]
        times[0] = tmp
        if who_won == 1:
            who_won = 2
        elif who_won == 2:
            who_won = 1
    return who_won, times

def check_n_times(algorithms: List[TicTacToeAlgorithm], n: int, random_places = False) -> Tuple[int, int, int, List[float]]:
    ''' Play n games.'''
    wins = 0  # player_1 wins
    loses = 0  # player_1 loses
    ties = 0
    times_total = [0.0, 0.0]
    for i in range(n):
        if randint(0, 1) == 1 and random_places:  # randomly change places of two algorithms (switch sides)
            change_places = True
        else:
            change_places = False
        # board: 0 = empty, 1 = player_1, 2 = player_2
        board = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        result, times = play(board, algorithms, change_places)
        times_total[0] += times[0]
        times_total[1] += times[1]
        if result == 1:
            wins += 1
        elif result == 2:
            loses += 1
        elif result == 3:
            ties += 1
    times_total[0] /= n
    times_total[1] /= n
    return (wins, loses, ties, times_total)

def print_results(algorithms: List[TicTacToeAlgorithm], wins, loses, ties, times: List[int], end = "\n"):
    ''' Display the results.'''
    print(f"{algorithms[0].get_algo_name()} wins: {wins}", f"{algorithms[1].get_algo_name()} wins: {loses}", f"ties: {ties}",
        f"average game time: {algorithms[0].get_algo_name()} - {times[0]:.9f},", f"{algorithms[1].get_algo_name()} - {times[1]:.9f}", end = end)

if __name__ == "__main__":
    algorithms = [None, None]

    start = timer()
    # the bruteforce "tree" array is always the same, so it can be created once, saved to a file and resued
    BruteforceAlgorithm(save = 1)
    end = timer()
    print('Time for bruteforce initialization:', f"{(end - start):.9f}")

    # a vs b (random vs bruteforce)
    algorithms[1] = BruteforceAlgorithm(load = 1)
    algorithms[0] = RandomAlgorithm()
    wins, loses, ties, times = check_n_times(algorithms, n = 100, random_places = True)
    print_results(algorithms, wins, loses, ties, times)

    # a vs c (random vs minimax)
    for i in range(1, 10):  # check all max depths from 1 to 9 
        algorithms[0] = RandomAlgorithm()
        algorithms[1] = MinimaxAlgorithm(max_depth = i)
        wins, loses, ties, times = check_n_times(algorithms, n = 100)
        print_results(algorithms, wins, loses, ties, times, end = "")
        print(f" (max depth = {i})")


    # b vs c (bruteforce vs minimax)
    for i in range(1, 10):
        algorithms[0] = BruteforceAlgorithm(load = 1)
        algorithms[1] = MinimaxAlgorithm(max_depth = i)
        wins, loses, ties, times = check_n_times(algorithms, n = 1)
        print_results(algorithms, wins, loses, ties, times, end = "")
        print(f" (max depth = {i})")

    # c vs b (minimax vs bruteforce)
    for i in range(1, 10):
        algorithms[0] = MinimaxAlgorithm(max_depth = i)
        algorithms[1] = BruteforceAlgorithm(load = 1)
        wins, loses, ties, times = check_n_times(algorithms, n = 1)
        print_results(algorithms, wins, loses, ties, times, end = "")
        print(f" (max depth = {i})")
