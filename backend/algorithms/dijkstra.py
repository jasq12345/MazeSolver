"""Dijkstra's Algorithm.

Owner: Person 1

Data structures:
  - Priority queue (heapq) of (cost, cell) -> cell with the lowest cost first
  - Dictionary cost                        -> best known cost from start
  - Dictionary parent                      -> where each cell was reached from
  - Set explored                           -> cells already finalized
  - List visited                           -> exploration order (for frontend)

Every step costs 1 here, so Dijkstra finds the same path length as BFS - but
it's the algorithm that still works once steps have different costs.
"""

import heapq
from math import inf

from algorithms.utils import Grid, Position, SearchResult, get_neighbors, reconstruct_path


def dijkstra(grid: Grid, start: Position, goal: Position) -> SearchResult:
    """Run Dijkstra from `start` to `goal`.

    Returns:
        SearchResult(visited, path)
        visited -> cells in the exact order they were explored
        path    -> shortest route start -> goal (maze is always solvable)
    """
    heap: list[tuple[int, Position]] = [(0, start)]
    cost: dict[Position, int] = {start: 0}
    parent: dict[Position, Position | None] = {start: None}
    explored: set[Position] = set()
    visited: list[Position] = []

    while heap:
        current_cost, current = heapq.heappop(heap)

        if current in explored:
            continue
        explored.add(current)
        visited.append(current)

        if current == goal:
            break

        for neighbor in get_neighbors(grid, current):
            new_cost = current_cost + 1
            if new_cost < cost.get(neighbor, inf):
                cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(heap, (new_cost, neighbor))

    return SearchResult(visited, reconstruct_path(parent, start, goal))
