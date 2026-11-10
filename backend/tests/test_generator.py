"""Tests for maze generation.  Owner: Backend 3"""

import random

import pytest

from algorithms.bfs import bfs
from algorithms.utils import OPEN, WALL
from maze.generator import generate_maze


def test_size_start_and_goal():
    grid, start, goal = generate_maze(8, 12)
    assert len(grid) == 8
    assert all(len(row) == 12 for row in grid)
    assert start == (0, 0)
    assert goal == (7, 11)


def test_cells_are_open_or_wall():
    grid, _, _ = generate_maze(15, 15)
    assert all(cell in (OPEN, WALL) for row in grid for cell in row)


def test_first_row_and_last_column_open():
    grid, _, _ = generate_maze(10, 10, wall_density=0.9)
    assert all(cell == OPEN for cell in grid[0])
    assert all(row[-1] == OPEN for row in grid)


def test_wall_density_is_roughly_respected():
    random.seed(0)
    grid, _, _ = generate_maze(50, 50, wall_density=0.3)
    # only the inner cells are random (first row + last column are forced open)
    inner = [cell for row in grid[1:] for cell in row[:-1]]
    assert 0.25 < sum(inner) / len(inner) < 0.35


def test_always_solvable():
    for seed in range(200):
        random.seed(seed)
        grid, start, goal = generate_maze(random.randint(2, 30), random.randint(2, 30))
        path = bfs(grid, start, goal).path
        assert path[0] == start and path[-1] == goal


def test_invalid_arguments():
    with pytest.raises(ValueError):
        generate_maze(0, 5)
    with pytest.raises(ValueError):
        generate_maze(5, 5, wall_density=1.5)
