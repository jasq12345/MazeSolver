"""Random maze generation (random obstacles, not a full maze algorithm).

Owner: Backend 3
"""

import random

from algorithms.utils import OPEN, WALL, Grid, Position


def generate_maze(
    rows: int = 20, cols: int = 20, wall_density: float = 0.3
) -> tuple[Grid, Position, Position]:
    """Generate a random maze that always has a route start -> goal.

    Returns:
        (grid, start, goal)
        start -> top-left corner (0, 0)
        goal  -> bottom-right corner (rows - 1, cols - 1)

    The first row and the last column are always open, so you can always walk
    right along the top and then down the right side: the maze is solvable.
    """
    if rows < 1 or cols < 1:
        raise ValueError("rows and cols must be at least 1")
    if not 0 <= wall_density <= 1:
        raise ValueError("wall_density must be between 0 and 1")

    grid = [
        [WALL if random.random() < wall_density else OPEN for _ in range(cols)]
        for _ in range(rows)
    ]

    for col in range(cols):  # first row open
        grid[0][col] = OPEN
    for row in range(rows):  # last column open
        grid[row][cols - 1] = OPEN

    return grid, (0, 0), (rows - 1, cols - 1)
