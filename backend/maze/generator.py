"""Random maze generation (random obstacles, not a full maze algorithm).

Owner: Backend 3
"""

from algorithms.utils import Grid, Position


def generate_maze(
    rows: int = 20, cols: int = 20, wall_density: float = 0.3
) -> tuple[Grid, Position, Position]:
    """Generate a random maze that always has a route start -> goal.

    Returns:
        (grid, start, goal)
        start -> top-left corner (0, 0)
        goal  -> bottom-right corner (rows - 1, cols - 1)

    TODO (Backend 3):
      1. Create a rows x cols matrix.
      2. Randomly set each cell to WALL or OPEN (~wall_density walls).
      3. Keep the first row fully open.
      4. Keep the last column fully open.
         (3 + 4 guarantee a route from top-left to bottom-right.)
      5. Return (grid, (0, 0), (rows - 1, cols - 1)).
    """
    raise NotImplementedError
