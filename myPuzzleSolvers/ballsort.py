"""Ballsort Puzzle Solver

"""

import logging
import json
from time import localtime, time, asctime
import sys
import os

from mySearchAlgorithms import UniformCostSearch, AStarSearch
from puzzle_boards import ballsort_puzzle_boards

module_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(module_path))

TIME = asctime(localtime(time()))

output_path = os.path.join(module_path, 'Ballsort_Output')
if not os.path.exists(output_path):
    os.mkdir(output_path)
log_file = os.path.join(output_path, f"outputs_{TIME}.log")

ALGORITHM = ""

logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO)
logger = logging.getLogger()


def goal_test(node):
    """Tests if goal is satisfied

    Args:
        node (dict): Node includes the representation for each state

    Returns:
        bool: True if goal is satisfied
    """
    for row in node['state']:
        if any(element != row[0] for element in row):
            return False
    return True


def successor_function(node):
    """Generates child nodes which are successors of parent node

    Args:
        node (dict): Parent node

    Returns:
        list: List of child nodes
    """
    state = node['state']  # pylint: disable=redefined-outer-name
    path = node['path']
    tube_count = len(state)

    child_nodes = list()

    for first_row_idx in range(tube_count):

        first_row = state[first_row_idx]
        first_ball_idx = 0
        for ball in first_row:
            if ball == -1:
                break
            else:
                first_ball_idx += 1
        first_ball_idx -= 1

        if(first_ball_idx != -1 and
                any(element != first_row[0] or element == -1 for element in first_row)):

            for sec_row_idx in range(tube_count):
                if first_row_idx != sec_row_idx:
                    second_row = state[sec_row_idx]
                    if any(element != second_row[0] or element == -1 for element in second_row):
                        second_ball_idx = 0
                        for ball in second_row:
                            if ball == -1:
                                break
                            else:
                                second_ball_idx += 1

                        if second_ball_idx != 4:

                            if second_ball_idx == 0 or \
                                    first_row[first_ball_idx] == second_row[second_ball_idx-1]:

                                new_state = [i[:] for i in state]

                                new_state[sec_row_idx][second_ball_idx] = \
                                    state[first_row_idx][first_ball_idx]
                                new_state[first_row_idx][first_ball_idx] = -1
                                new_path = [i for i in path]
                                new_path.append(node['id'])
                                new_cost, heuristic_cost = step_cost_function(
                                    node['cost'], new_state)
                                child_node = {
                                    'id': -1,
                                    'cost': new_cost,
                                    'path': new_path,
                                    'state': new_state,
                                    'heuristic': heuristic_cost
                                }
                                child_nodes.append(child_node)
    return child_nodes


def step_cost_function(cost, new_state):
    """[summary]

    Args:
        cost ([type]): [description]
        new_state ([type]): [description]

    Returns:
        [type]: [description]
    """
    if ALGORITHM == "ucs":
        return cost+1, 0
    elif ALGORITHM == "ass":
        return cost+1, heuristic_function(new_state)
    else:
        cost+1, 0  # pylint: disable=pointless-statement


def heuristic_function(new_state):
    """Heuristic is calculated

    Args:
        new_state (list): A list of lists describing state

    Returns:
        int: Heuristic cost
    """
    heuristic_cost = 0
    for row in new_state:
        if -1 in row:
            first_item = row[0]
            for item in row:
                if(item != first_item and item != -1):
                    heuristic_cost += 1
    return heuristic_cost


def take_input():
    """Take state input from user

    Returns:
        state: A list of lists to define state
    """
    state = list()  # pylint: disable=redefined-outer-name
    f, e = map(int, input("Enter a full and empty bottle numbers: ")\
               .split())  # pylint: disable=redefined-outer-name disable=invalid-name
    for _ in range(f):
        input_colors = map(int, input("Enter colors of numbers: ").split())
        state.append(input_colors)

    return state, e


def take_test_board(test, idx):  # pylint: disable=redefined-outer-name
    """Take state from a test board of a test list from tests module

    Args:
        test (list): Test board list
        idx (int): Test board id

    Returns:
        list: A list of lists defining state
    """
    board = test[idx]
    e = board[0][1]  # pylint: disable=redefined-outer-name disable=invalid-name

    state = list()  # pylint: disable=redefined-outer-name
    for row in board[1:]:
        state.append(row)

    return state, e


if __name__ == '__main__':

    #state, e = take_input()

    test = ballsort_puzzle_boards.test_boards
    TEST_COUNT = len(test)

    for idx in range(TEST_COUNT):
        state, e = take_test_board(test, idx)
        for e in range(e):
            emptylist = [-1]*4
            state.append(emptylist)

        # UNIFORM COST SEARCH

        initial_node = {
            'id': 0,
            'cost': 0,
            'path': [],
            'state': state
        }

        start_time = time()
        logger.info("%s", '-'*30)
        logger.info(
            "START UNIFORM-COST SEARCH TIME: %s for %d", asctime(localtime(start_time)), idx)
        logger.info("%s", '-'*30)
        ALGORITHM = "ucs"
        UCS = UniformCostSearch(successor_function, goal_test)
        result = UCS.search(initial_node)
        finish_time = time()
        logger.info(
            "FINISH UCS TIME: %s for %d", asctime(localtime(finish_time)), idx)
        logger.info("TIME DIFFERENCE: %f", (finish_time - start_time))
        ucs_output_filename = f"output_{TIME}_ucs_{idx}.out.json"
        with open(os.path.join(output_path, ucs_output_filename), 'w', encoding="utf-8") as outfile:
            json.dump(result, outfile)

        # A-STAR SEARCH

        initial_node = {
            'id': 0,
            'cost': 0,
            'heuristic': 0,
            'path': [],
            'state': state
        }

        start_time = time()
        logger.info("%s", '-'*30)
        logger.info(
            "START A* SEARCH TIME: %s for %d", asctime(localtime(start_time)), idx)
        logger.info("%s", '-'*30)
        ALGORITHM = "ass"
        ASS = AStarSearch(successor_function, goal_test)
        initial_node['heuristic'] = heuristic_function(initial_node['state'])
        result = ASS.search(initial_node)
        finish_time = time()
        logger.info(
            "FINISH A* TIME: %s for %d", asctime(localtime(finish_time)), idx)
        logger.info("TIME DIFFERENCE: %f", (finish_time - start_time))
        ass_output_filename = f"output_{TIME}_ass_{idx}.out.json"
        with open(os.path.join(output_path, ass_output_filename), 'w', encoding="utf-8") as outfile:
            json.dump(result, outfile)
