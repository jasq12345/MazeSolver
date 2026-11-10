"""Tests for A*.  Owner: Person 2

Remove the skip marker once astar.py is implemented.
Tip: look at tests/test_dfs.py - it has an `assert_valid_path` helper you can copy.
"""

import pytest

pytestmark = pytest.mark.skip(reason="A* not implemented yet")

SIMPLE_GRID = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]

# Open 5x5 room: A* should go almost straight to the goal.
OPEN_GRID = [[0] * 5 for _ in range(5)]

START = (0, 0)
GOAL = (4, 4)


def test_manhattan_distance():
    """TODO: (0, 0) -> (3, 4) is 7; same cell is 0; order of arguments doesn't matter."""


def test_astar_finds_a_path():
    """TODO: path starts at START and ends at GOAL."""


def test_astar_path_is_connected():
    """TODO: every step moves exactly one cell and never goes through a wall (SIMPLE_GRID and OPEN_GRID)."""


def test_astar_path_is_shortest():
    """TODO: len(astar(...).path) == len(bfs(...).path) on SIMPLE_GRID, OPEN_GRID
    and ~100 random mazes from generate_maze (use random.seed so failures repeat)."""


def test_astar_visits_fewer_cells_than_bfs():
    """TODO: on OPEN_GRID, len(astar(...).visited) < len(bfs(...).visited)  (9 vs 25)."""


def test_astar_visited_has_no_duplicates():
    """TODO: each cell appears at most once in visited."""


def test_astar_visited_order():
    """TODO: visited[0] == START, visited[-1] == GOAL, every path cell is in visited."""


def test_astar_start_equals_goal():
    """TODO: start == goal -> path == [START] and visited == [START]."""
