"""Tests for BFS and graph utilities.  Owner: Backend 1

Remove the skip marker once bfs.py / utils.py are implemented.
"""

from algorithms.bfs import bfs
from algorithms.utils import (
    get_neighbors,
    is_valid,
    reconstruct_path
)

SIMPLE_GRID = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]


def test_is_valid_inside_and_walls():
    """TODO: in-bounds open cell -> True, wall -> False, out of bounds -> False."""
    assert is_valid(SIMPLE_GRID, (0,0)) is True
    assert is_valid(SIMPLE_GRID, (0,2)) is False
    assert is_valid(SIMPLE_GRID, (0,5)) is False
    assert is_valid(SIMPLE_GRID, (-1, 0)) is False

def test_get_neighbors():
    """TODO: corner, edge and middle cells return only valid neighbors."""  # up, down, left, right
    assert get_neighbors(SIMPLE_GRID, (1,1))  == [(0,1), (2,1)]
    assert get_neighbors(SIMPLE_GRID, (0,0)) == [(0,1)]


def test_reconstruct_path():
    """TODO: use the parent table from the guideline -> [(0,0),(0,1),(1,1),(2,1),(2,2)]."""
    parent = {
        (0, 0): None,
        (0, 1): (0, 0),
        (1, 1): (0, 1),
        (2, 1): (1, 1),
        (2, 2): (2, 1),
    }
    assert reconstruct_path(parent, (0, 0), (2, 2)) == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]


def test_bfs_finds_shortest_path():
    """TODO: path starts at start, ends at goal, and has minimal length."""
    result = bfs(SIMPLE_GRID, (0, 0), (2, 2))

    assert result.path[0] == (0, 0)
    assert result.path[-1] == (2, 2)
    assert result.path == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
    assert len(result.path) == 5


def test_bfs_start_equals_goal():
    """TODO: start == goal -> path == [start]."""
    result = bfs(SIMPLE_GRID, (0, 0), (0, 0))
    assert result.path == [(0, 0)]
