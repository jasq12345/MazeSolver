# Maze Solver – Backend

FastAPI server that generates mazes and solves them with graph search algorithms.
For project overview and full setup (incl. frontend) see the [main README](../README.md).

## Quick start

```bash
cd backend
uv sync                            # install packages (incl. pytest, httpx)
uv run uvicorn main:app --reload   # http://localhost:8000, interactive docs at /docs
uv run pytest                      # run all tests
```

`test_main.http` contains ready-made requests you can run from PyCharm.

## Code structure

```
backend/
├── main.py               # FastAPI app: endpoints, validation, CORS
├── pyproject.toml        # dependencies (managed by uv)
├── uv.lock               # exact versions – commit it
├── test_main.http        # manual API requests
├── algorithms/
│   ├── utils.py          # shared types, is_valid, get_neighbors, reconstruct_path, SearchResult
│   ├── bfs.py            # Breadth-First Search
│   ├── dfs.py            # Depth-First Search
│   ├── dijkstra.py       # Dijkstra            🚧 Person 1
│   └── astar.py          # A*                  🚧 Person 2
├── maze/
│   └── generator.py      # random solvable maze
└── tests/
    ├── test_bfs.py       # BFS + utils
    ├── test_dfs.py
    ├── test_dijkstra.py  # 🚧 Person 1
    ├── test_astar.py     # 🚧 Person 2
    ├── test_generator.py
    └── test_api.py       # endpoint tests (FastAPI TestClient)
```

## Shared interfaces

Don't change these without telling the team – every algorithm and the frontend depend on them.

**Maze**: 2D list, `grid[row][col]`, `0` = walkable (`OPEN`), `1` = wall (`WALL`).
**Position**: `(row, col)` tuple. Moves: up `(-1,0)`, down `(1,0)`, left `(0,-1)`, right `(0,1)` (`DIRECTIONS`).
**Every maze is solvable**: the generator keeps the first row and the last column open, so there is always a route from the top-left to the bottom-right corner.

| Function | File | Signature | Returns |
|---|---|---|---|
| `is_valid` | `algorithms/utils.py` | `(grid, position)` | `bool` – inside grid and not a wall |
| `get_neighbors` | `algorithms/utils.py` | `(grid, position)` | `list[Position]` – valid neighbors |
| `reconstruct_path` | `algorithms/utils.py` | `(parent, start, goal)` | `list[Position]` – start→goal |
| `bfs` / `dfs` | `algorithms/bfs.py`, `dfs.py` | `(grid, start, goal)` | `SearchResult` |
| `dijkstra` / `astar` | `algorithms/dijkstra.py`, `astar.py` | `(grid, start, goal)` | `SearchResult` |
| `generate_maze` | `maze/generator.py` | `(rows=20, cols=20, wall_density=0.3)` | `(grid, start, goal)` |

`SearchResult` (dataclass in `algorithms/utils.py`):

- `visited` – cells in the exact order they were explored, each cell once (the frontend animates this)
- `path` – cells from start to goal

**Every search algorithm must:** use `get_neighbors` (no own neighbor logic), use `reconstruct_path`, return a `SearchResult`, and stop as soon as the goal is explored.

## API

| Method | Endpoint | Body / Query | Response |
|---|---|---|---|
| GET | `/api/health` | – | `{"status": "ok", "message": ...}` |
| GET | `/api/maze/generate` | `?rows=&cols=&wall_density=` | `{grid, start, goal}` |
| POST | `/api/solve/bfs` | `{grid, start, goal}` | `{visited, path, visited_count, path_length, execution_time_ms}` |
| POST | `/api/solve/dfs` | `{grid, start, goal}` | same as above |
| POST | `/api/solve/dijkstra` 🚧 | `{grid, start, goal}` | same as above |
| POST | `/api/solve/astar` 🚧 | `{grid, start, goal}` | same as above |

- `path_length` = number of cells in `path`; `visited_count` = number of cells in `visited`; `execution_time_ms` = time of the algorithm only (not validation or JSON).
- `/api/maze/generate` limits: `rows` and `cols` 2–100, `wall_density` 0–0.9 (defaults 20, 20, 0.3). Out of range → `422`.
- `/api/solve/*` returns `400` with `{"detail": "..."}` when the grid is empty, not rectangular or has values other than 0/1, when start or goal is outside the grid or on a wall, or when the maze can't be solved (possible when the user draws walls in the frontend).
- CORS allows `http://localhost:5173` / `:3000` (and `127.0.0.1`).

## How to add a new algorithm

1. Create `algorithms/<name>.py` with `def <name>(grid, start, goal) -> SearchResult`.
2. Add tests in `tests/test_<name>.py`.
3. Add an endpoint in `main.py` – it's 3 lines, `solve()` already does validation, timing and the response:
   ```python
   @app.post("/api/solve/<name>", response_model=SolveResponse)
   def solve_<name>(request: MazeRequest):
       return solve(request, <name>)
   ```
4. Add `"<name>"` to the `@pytest.mark.parametrize("algorithm", [...])` lists in `tests/test_api.py`.
5. Add a request to `test_main.http`.
6. Tell the frontend team the new endpoint name (they add it to `src/services/api.js` and the algorithm dropdown).

---

## Tasks

Each person works only in their own files and on their own branch (`dijkstra`, `astar`), merged via pull request.
`main.py`, `tests/test_api.py` and `test_main.http` are touched by both people (a few lines each) – **merge Dijkstra first**, then the A* person updates their branch from `main` (`git pull origin main`) before opening their PR.

### ✅ Phase 1 – done

- **Backend 1** – `utils.py` (`is_valid`, `get_neighbors`, `reconstruct_path`) + BFS + tests
- **Backend 2** – DFS + tests
- **Backend 3** – uv setup, maze generator, FastAPI endpoints, validation, CORS + tests

### 👤 Person 1 — Dijkstra

Files: `algorithms/dijkstra.py`, `tests/test_dijkstra.py` (+ a few lines in `main.py`, `tests/test_api.py`, `test_main.http`)

Dijkstra always expands the cell with the **lowest total cost from the start** so far. It uses a **priority queue** (`heapq`) instead of a plain queue. In our maze every step costs 1, so it finds the same path length as BFS – but it's the algorithm that still works when steps have different costs (see stretch goal).

| Data structure | Purpose |
|---|---|
| Priority queue (`heapq`) of `(cost, cell)` | cell with the lowest cost is popped first |
| Dictionary `cost` | best known cost from start to each cell |
| Dictionary `parent` | where each cell was reached from |
| Set `explored` | cells already finalized |
| List `visited` | exploration order for the frontend |

- [ ] Create `algorithms/dijkstra.py` with `dijkstra(grid, start, goal) -> SearchResult`
- [ ] Start with `heap = [(0, start)]`, `cost = {start: 0}`, `parent = {start: None}`
- [ ] Loop: `heappop` the lowest-cost cell; if it's already in `explored` → skip it (it was pushed twice, the old entry is outdated)
- [ ] Mark it explored, append to `visited`, stop if it's the goal
- [ ] For each cell from `get_neighbors`: `new_cost = cost[current] + 1`; if it's lower than `cost.get(neighbor, inf)` → update `cost`, `parent`, and `heappush((new_cost, neighbor))`
- [ ] Return `SearchResult(visited, reconstruct_path(parent, start, goal))`
- [ ] Tests in `tests/test_dijkstra.py`:
  - path starts at start, ends at goal, moves one step at a time, never through a wall
  - path length equals BFS path length (both are optimal) on several grids, incl. random ones from `generate_maze`
  - `visited` has no duplicates, starts with start, ends with goal
  - start == goal → `path == [start]`
- [ ] Add `POST /api/solve/dijkstra` in `main.py` (see [How to add a new algorithm](#how-to-add-a-new-algorithm))
- [ ] Add `"dijkstra"` to the parametrize lists in `tests/test_api.py` and a request to `test_main.http`
- [ ] `uv run pytest` passes, update the 🚧 markers in both READMEs
- [ ] ⭐ Stretch goal (discuss with the team first – changes the maze format): weighted cells, e.g. `2–9` = mud/water with that step cost. Then Dijkstra finds cheaper paths than BFS. Needs changes in `validate_maze`, the generator and the frontend.

### 👤 Person 2 — A*

Files: `algorithms/astar.py`, `tests/test_astar.py` (+ a few lines in `main.py`, `tests/test_api.py`, `test_main.http`)

A* is Dijkstra with a sense of direction. It orders the priority queue by `f = g + h`:
`g` = cost from start so far, `h` = **heuristic** estimate of the remaining distance to the goal.
We use the **Manhattan distance** `|r1 - r2| + |c1 - c2|` – it never overestimates on a 4-direction grid, so A* still finds the shortest path, but it explores far fewer cells because it heads towards the goal.

| Data structure | Purpose |
|---|---|
| Priority queue (`heapq`) of `(f, h, cell)` | lowest `f` first; on a tie, the cell closer to the goal (`h`) first |
| Dictionary `g` | best known cost from start to each cell |
| Dictionary `parent` | where each cell was reached from |
| Set `explored` | cells already finalized |
| List `visited` | exploration order for the frontend |

- [ ] Create `algorithms/astar.py` with `manhattan_distance(a, b) -> int` and `astar(grid, start, goal) -> SearchResult`
- [ ] Start with `heap = [(h(start), h(start), start)]`, `g = {start: 0}`, `parent = {start: None}`
- [ ] Loop: `heappop`; if already in `explored` → skip; mark explored, append to `visited`, stop at the goal
- [ ] For each cell from `get_neighbors`: `new_g = g[current] + 1`; if lower than `g.get(neighbor, inf)` → update `g`, `parent`, `heappush((new_g + h, h, neighbor))`
- [ ] Return `SearchResult(visited, reconstruct_path(parent, start, goal))`
- [ ] Tests in `tests/test_astar.py`:
  - `manhattan_distance((0, 0), (3, 4)) == 7`, and `0` for the same cell
  - path starts at start, ends at goal, moves one step at a time, never through a wall
  - path length equals BFS path length (A* is optimal) on several grids, incl. random ones from `generate_maze`
  - on an open grid with no walls A* visits **fewer** cells than BFS
  - `visited` has no duplicates, starts with start, ends with goal
  - start == goal → `path == [start]`
- [ ] Add `POST /api/solve/astar` in `main.py`
- [ ] Add `"astar"` to the parametrize lists in `tests/test_api.py` and a request to `test_main.http`
- [ ] `uv run pytest` passes, update the 🚧 markers in both READMEs
- [ ] ⭐ Stretch goal: once Dijkstra is merged, add a test that A* never visits more cells than Dijkstra on random mazes

### Frontend follow-up (after both PRs are merged)

- [ ] `src/services/api.js`: add `solveDijkstra` and `solveAStar` (same as `solveBFS`, different URL)
- [ ] `src/components/controls.jsx`: add `Dijkstra` and `A*` to the algorithm dropdown
- [ ] `src/App.jsx`: pick the right solver for the selected algorithm
