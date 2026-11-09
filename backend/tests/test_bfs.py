"""Tests for BFS and graph utilities.  Owner: Backend 1

Remove the skip marker once bfs.py / utils.py are implemented.
"""

import pytest

pytestmark = pytest.mark.skip(reason="BFS not implemented yet")

SIMPLE_GRID = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]


def test_is_valid_inside_and_walls():
    """TODO: in-bounds open cell -> True, wall -> False, out of bounds -> False."""


def test_get_neighbors():
    """TODO: corner, edge and middle cells return only valid neighbors."""


def test_reconstruct_path():
    """TODO: use the parent table from the guideline -> [(0,0),(0,1),(1,1),(2,1),(2,2)]."""


def test_bfs_finds_shortest_path():
    """TODO: path starts at start, ends at goal, and has minimal length."""


def test_bfs_start_equals_goal():
    """TODO: start == goal -> path == [start]."""
