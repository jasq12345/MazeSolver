"""Tests for DFS.  Owner: Backend 2"""

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.utils import WALL

SIMPLE_GRID = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]

# Open 5x5 room: many possible routes, so DFS usually won't find the shortest one.
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


def test_dfs_finds_a_path():
    result = dfs(SIMPLE_GRID, START, GOAL)
    assert result.path[0] == START
    assert result.path[-1] == GOAL


def test_dfs_path_is_connected():
    for grid in (SIMPLE_GRID, OPEN_GRID):
        result = dfs(grid, START, GOAL)
        assert_valid_path(grid, result.path, START, GOAL)


def test_dfs_path_has_no_repeated_cells():
    result = dfs(OPEN_GRID, START, GOAL)
    assert len(result.path) == len(set(result.path))


def test_dfs_visited_has_no_duplicates():
    for grid in (SIMPLE_GRID, OPEN_GRID):
        result = dfs(grid, START, GOAL)
        assert len(result.visited) == len(set(result.visited))


def test_dfs_visited_order():
    result = dfs(SIMPLE_GRID, START, GOAL)
    assert result.visited[0] == START
    assert result.visited[-1] == GOAL  # stops as soon as the goal is explored
    assert set(result.path) <= set(result.visited)


def test_dfs_visited_never_contains_walls():
    result = dfs(SIMPLE_GRID, START, GOAL)
    for r, c in result.visited:
        assert SIMPLE_GRID[r][c] != WALL


def test_dfs_path_not_shorter_than_bfs():
    """BFS is optimal, so DFS can match it but never beat it."""
    for grid in (SIMPLE_GRID, OPEN_GRID):
        assert len(dfs(grid, START, GOAL).path) >= len(bfs(grid, START, GOAL).path)


def test_dfs_goes_deep_first():
    """In an open room DFS follows one direction instead of spreading level by level."""
    result = dfs(OPEN_GRID, START, GOAL)
    bfs_result = bfs(OPEN_GRID, START, GOAL)
    assert result.visited != bfs_result.visited


def test_dfs_start_equals_goal():
    result = dfs(SIMPLE_GRID, START, START)
    assert result.path == [START]
    assert result.visited == [START]
