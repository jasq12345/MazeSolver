"""Depth-First Search.

Owner: Backend 2

Data structures:
  - Stack (list)  -> cells waiting to be explored
  - Set           -> cells already visited
  - Dictionary    -> parent of each discovered cell
  - List          -> exploration order (for frontend animation)

Difference from BFS: uses a stack and removes the LAST element, so it goes
deep before backtracking. DFS does NOT guarantee the shortest path.
"""
from algorithms.utils import Grid, Position, SearchResult, get_neighbors, reconstruct_path


def dfs(grid: Grid, start: Position, goal: Position) -> SearchResult:
    """Run DFS from `start` to `goal`.

    Returns:
        SearchResult(visited, path)
        visited -> cells in the exact order they were explored
        path    -> a route start -> goal (not necessarily shortest; maze is always solvable)

    TODO (Backend 2):
      1. Initialize a stack containing the start position.
      2. Mark the start as visited (keep a separate set).
      3. Create parent dict: {start: None}.
      4. Pop the LAST element of the stack.
      5. Append it to `visited`; if it is the goal, stop.
      6. For each neighbor in get_neighbors(grid, current):
      7.   if not visited -> push to stack,
      8.   record parent[neighbor] = current.
      9. Return SearchResult(visited, reconstruct_path(parent, start, goal)).

    Note: `visited` must reflect the real exploration order (frontend animates it).
    """
    stack = [start]
    explored: set[Position] = set()  # fast "already visited?" check
    visited: list[Position] = []     # exploration order for the frontend
    parent: dict[Position, Position | None] = {start: None}

    while stack:
        current = stack.pop()  # LAST element -> depth-first

        # A cell can be pushed more than once before it is explored;
        # only the first pop counts.
        if current in explored:
            continue
        explored.add(current)
        visited.append(current)

        if current == goal:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in explored:
                # Overwriting is fine: the newest push is popped first,
                # so the parent always matches the cell that reached it.
                parent[neighbor] = current
                stack.append(neighbor)

    return SearchResult(visited, reconstruct_path(parent, start, goal))
