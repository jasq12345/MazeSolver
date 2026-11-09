"""Shared graph utilities used by BFS and DFS.

Owner: Backend 1 (reconstruct_path shared with Backend 2)

The maze is a 2D matrix (list of rows). Every walkable cell is a vertex;
two vertices are connected when they are adjacent up/down/left/right.
The graph is undirected, unweighted and not necessarily fully connected.
Neighbors are computed on the fly - no adjacency list is built.
"""

# ---- Shared types (agreed interface - do not change without telling the team) ----
Position = tuple[int, int]  # (row, col)
Grid = list[list[int]]      # grid[row][col]

OPEN = 0  # walkable cell
WALL = 1  # wall

# Up, Down, Left, Right as (d_row, d_col)
DIRECTIONS: list[Position] = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_valid(grid: Grid, position: Position) -> bool:
    """Return True if `position` is inside the grid and is not a wall.

    TODO (Backend 1):
      1. Check the position is inside the maze boundaries.
      2. Check the position is not a wall.
    """
    raise NotImplementedError


def get_neighbors(grid: Grid, position: Position) -> list[Position]:
    """Return all valid neighbors (up, down, left, right) of `position`.

    TODO (Backend 1):
      1. Build the four adjacent cells using DIRECTIONS.
      2. Keep only the ones for which is_valid() is True.
      3. Return them as a list.

    Both BFS and DFS MUST use this function - do not duplicate neighbor logic.
    """
    raise NotImplementedError


def reconstruct_path(
    parent: dict[Position, Position | None], start: Position, goal: Position
) -> list[Position]:
    """Rebuild the route from `start` to `goal` using the parent dictionary.

    The maze is always solvable, so `goal` is guaranteed to be in `parent`.

    TODO (Backend 1, reviewed by Backend 2):
      1. Walk backwards from `goal` following parent links until None.
      2. Reverse the list so it goes start -> goal.
    """
    raise NotImplementedError
