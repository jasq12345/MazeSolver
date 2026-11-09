"""Breadth-First Search.

Owner: Backend 1

Data structures:
  - Queue (collections.deque) -> cells waiting to be explored
  - Set                       -> cells already discovered
  - Dictionary                -> parent of each discovered cell
  - List                      -> exploration order (for frontend animation)
"""

from algorithms.utils import Grid, Position, get_neighbors, reconstruct_path


def bfs(grid: Grid, start: Position, goal: Position) -> tuple[list[Position], list[Position]]:
    """Run BFS from `start` to `goal`.

    Returns:
        (visited, path)
        visited -> cells in the exact order they were explored
        path    -> shortest route start -> goal (maze is always solvable)

    TODO (Backend 1):
      1. Initialize a queue containing the start position.
      2. Mark the start as visited.
      3. Create parent dict: {start: None}.
      4. Pop the FIRST element of the queue (popleft).
      5. Append it to `visited`; if it is the goal, stop.
      6. For each cell in get_neighbors(grid, current):
      7.   if not seen -> mark seen, add to queue,
      8.   record parent[neighbor] = current.
      9. Return (visited, reconstruct_path(parent, start, goal)).
    """
    raise NotImplementedError
