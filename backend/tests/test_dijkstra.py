"""Tests for Dijkstra.  Owner: Person 1"""

import random

from algorithms.bfs import bfs
from algorithms.dijkstra import dijkstra
from algorithms.utils import WALL
from maze.generator import generate_maze

SIMPLE_GRID = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]

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


def test_dijkstra_finds_a_path():
    result = dijkstra(SIMPLE_GRID, START, GOAL)
    assert result.path[0] == START
    assert result.path[-1] == GOAL


def test_dijkstra_path_is_connected():
    for grid in (SIMPLE_GRID, OPEN_GRID):
        result = dijkstra(grid, START, GOAL)
        assert_valid_path(grid, result.path, START, GOAL)


def test_dijkstra_path_is_shortest():
    """Dijkstra is optimal, so its path length must match BFS's."""
    for grid in (SIMPLE_GRID, OPEN_GRID):
        assert len(dijkstra(grid, START, GOAL).path) == len(bfs(grid, START, GOAL).path)

    random.seed(0)
    for _ in range(100):
        grid, start, goal = generate_maze(10, 10, 0.3)
        assert len(dijkstra(grid, start, goal).path) == len(bfs(grid, start, goal).path)


def test_dijkstra_visited_has_no_duplicates():
    for grid in (SIMPLE_GRID, OPEN_GRID):
        result = dijkstra(grid, START, GOAL)
        assert len(result.visited) == len(set(result.visited))


def test_dijkstra_visited_order():
    result = dijkstra(SIMPLE_GRID, START, GOAL)
    assert result.visited[0] == START
    assert result.visited[-1] == GOAL
    assert set(result.path) <= set(result.visited)


def test_dijkstra_start_equals_goal():
    result = dijkstra(SIMPLE_GRID, START, START)
    assert result.path == [START]
    assert result.visited == [START]
