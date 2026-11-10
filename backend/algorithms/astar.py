"""A* Search.

Owner: Person 2

A* is Dijkstra with a sense of direction. Every cell in the priority queue
gets a score:

    f = g + h
    g -> real cost from the start to this cell (every step costs 1)
    h -> heuristic: estimated cost from this cell to the goal

The cell with the LOWEST f is explored first, so the search heads towards
the goal instead of spreading in every direction like BFS.

Heuristic: Manhattan distance |r1 - r2| + |c1 - c2|. On a grid where you can
only move up/down/left/right it never overestimates, so A* still finds the
SHORTEST path - while exploring far fewer cells than BFS.

Data structures:
  - Priority queue (heapq) of (f, h, cell) -> lowest f first; on a tie the
                                             cell closer to the goal (lower h)
  - Dictionary g                           -> best known cost from start
  - Dictionary parent                      -> where each cell was reached from
  - Set explored                           -> cells already finalized
  - List visited                           -> exploration order (for frontend)

Example (open 5x5 grid, start (0, 0), goal (4, 4)):
    BFS explores all 25 cells, A* explores only 9.
"""

import heapq
from math import inf

from algorithms.utils import Grid, Position, SearchResult, get_neighbors, reconstruct_path


def manhattan_distance(a: Position, b: Position) -> int:
    """Return the number of up/down/left/right steps between `a` and `b`, ignoring walls.

    Examples:
        manhattan_distance((0, 0), (3, 4)) -> 7
        manhattan_distance((2, 2), (2, 2)) -> 0
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: Grid, start: Position, goal: Position) -> SearchResult:
    """Run A* from `start` to `goal`.

    Returns:
        SearchResult(visited, path)
        visited -> cells in the exact order they were explored
        path    -> shortest route start -> goal (maze is always solvable)

    TODO (Person 2):
      1. h_start = manhattan_distance(start, goal).
      2. Initialize the heap: heap = [(h_start, h_start, start)]   # (f, h, cell)
      3. Create g = {start: 0}, parent = {start: None},
         explored = set(), visited = [].
      4. While the heap is not empty:
      5.   Pop the cell with the lowest f: _, _, current = heapq.heappop(heap).
      6.   If current is already in `explored` -> skip it (continue).
           (A cell can be pushed more than once when a cheaper route is
            found later; the old heap entry is outdated.)
      7.   Add current to `explored`, append it to `visited`.
      8.   If current == goal -> stop (break).
      9.   For each neighbor in get_neighbors(grid, current):
               new_g = g[current] + 1
               if new_g < g.get(neighbor, inf):
                   g[neighbor] = new_g
                   parent[neighbor] = current
                   h = manhattan_distance(neighbor, goal)
                   heapq.heappush(heap, (new_g + h, h, neighbor))
     10. Return SearchResult(visited, reconstruct_path(parent, start, goal)).

    Note: use get_neighbors and reconstruct_path from utils.py - do not write
    your own neighbor logic.
    """
    h_start = manhattan_distance(start, goal)
    heap: list[tuple[int, int, Position]] = [(h_start, h_start, start)]
    g: dict[Position, int] = {start: 0}
    parent: dict[Position, Position | None] = {start: None}
    explored: set[Position] = set()
    visited: list[Position] = []

    while heap:
        _, _, current = heapq.heappop(heap)

        if current in explored:
            continue
        explored.add(current)
        visited.append(current)

        if current == goal:
            break

        for neighbor in get_neighbors(grid, current):
            new_g = g[current] + 1
            if new_g < g.get(neighbor, inf):
                g[neighbor] = new_g
                parent[neighbor] = current
                h = manhattan_distance(neighbor, goal)
                heapq.heappush(heap, (new_g + h, h, neighbor))

    return SearchResult(visited, reconstruct_path(parent, start, goal))
