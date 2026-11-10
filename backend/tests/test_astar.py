"""Tests for A*.  Owner: Person 2"""

import random

from algorithms.astar import astar, manhattan_distance
from algorithms.bfs import bfs
from algorithms.utils import WALL
from maze.generator import generate_maze

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


def assert_valid_path(grid, path, start, goal):
    """Path goes start -> goal, moves one step at a time and never enters a wall."""
    assert path[0] == start
    assert path[-1] == goal
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        assert abs(r1 - r2) + abs(c1 - c2) == 1, f"jump from {(r1, c1)} to {(r2, c2)}"
    for r, c in path:
        assert grid[r][c] != WALL, f"path goes through wall at {(r, c)}"


def test_manhattan_distance():
    assert manhattan_distance((0, 0), (3, 4)) == 7
    assert manhattan_distance((2, 2), (2, 2)) == 0
    assert manhattan_distance((0, 0), (3, 4)) == manhattan_distance((3, 4), (0, 0))


def test_astar_finds_a_path():
    result = astar(SIMPLE_GRID, START, GOAL)
    assert result.path[0] == START
    assert result.path[-1] == GOAL


def test_astar_path_is_connected():
    for grid in (SIMPLE_GRID, OPEN_GRID):
        result = astar(grid, START, GOAL)
        assert_valid_path(grid, result.path, START, GOAL)


def test_astar_path_is_shortest():
    for grid in (SIMPLE_GRID, OPEN_GRID):
        assert len(astar(grid, START, GOAL).path) == len(bfs(grid, START, GOAL).path)

    random.seed(0)
    for _ in range(100):
        grid, start, goal = generate_maze(10, 10, 0.3)
        assert len(astar(grid, start, goal).path) == len(bfs(grid, start, goal).path)


def test_astar_visits_fewer_cells_than_bfs():
    assert len(astar(OPEN_GRID, START, GOAL).visited) < len(bfs(OPEN_GRID, START, GOAL).visited)


def test_astar_visited_has_no_duplicates():
    for grid in (SIMPLE_GRID, OPEN_GRID):
        result = astar(grid, START, GOAL)
        assert len(result.visited) == len(set(result.visited))


def test_astar_visited_order():
    result = astar(SIMPLE_GRID, START, GOAL)
    assert result.visited[0] == START
    assert result.visited[-1] == GOAL
    assert set(result.path) <= set(result.visited)


def test_astar_start_equals_goal():
    result = astar(SIMPLE_GRID, START, START)
    assert result.path == [START]
    assert result.visited == [START]
