"""Tests for DFS.  Owner: Backend 2

Remove the skip marker once dfs.py is implemented.
"""

import pytest

pytestmark = pytest.mark.skip(reason="DFS not implemented yet")

SIMPLE_GRID = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]


def test_dfs_finds_a_path():
    """TODO: path starts at start, ends at goal."""


def test_dfs_path_is_connected():
    """TODO: every consecutive pair in path differs by exactly one step and is not a wall."""


def test_dfs_visited_has_no_duplicates():
    """TODO: each cell appears at most once in visited."""


def test_dfs_unreachable_goal():
    """TODO: goal fully walled off -> path == []."""


def test_dfs_start_equals_goal():
    """TODO: start == goal -> path == [start]."""
