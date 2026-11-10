# Maze Solver

A maze is represented as a graph and solved with **BFS** and **DFS**. The backend (FastAPI) generates random mazes and returns the explored cells, the final path and statistics to the React frontend, which animates them.

## Architecture

```
React frontend
      │  HTTP / JSON
      ▼
FastAPI – API layer (main.py)          receive requests, validate input
      │
      ├── BFS  (algorithms/bfs.py)     queue
      ├── DFS  (algorithms/dfs.py)     stack
      ├── Maze generator (maze/generator.py)   random grid
      └── Graph utilities (algorithms/utils.py) neighbors + path reconstruction
      │
      ▼
JSON response: visited cells · final path · statistics
```

## Project structure

```
MazeSolver/
├── README.md
├── frontend/                 # React + Vite app
│   ├── package.json          # npm scripts + dependencies
│   ├── package-lock.json     # exact versions – commit it
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx          # entry point
│       ├── App.jsx
│       ├── components/       # MazeGrid, Controls, Statistics, Legend
│       └── services/api.js   # calls the backend (http://localhost:8000)
└── backend/
    ├── main.py               # FastAPI app + endpoints          (Backend 3)
    ├── pyproject.toml        # dependencies (managed by uv)
    ├── uv.lock               # exact versions – commit it
    ├── test_main.http        # manual API requests
    ├── algorithms/
    │   ├── __init__.py
    │   ├── utils.py          # is_valid, get_neighbors, reconstruct_path (Backend 1)
    │   ├── bfs.py            # BFS                               (Backend 1)
    │   └── dfs.py            # DFS                               (Backend 2)
    ├── maze/
    │   ├── __init__.py
    │   └── generator.py      # random maze generation           (Backend 3)
    └── tests/
        ├── __init__.py
        ├── test_bfs.py       # BFS + utils tests                 (Backend 1)
        ├── test_dfs.py       # DFS tests                         (Backend 2)
        ├── test_generator.py # maze generator tests              (Backend 3)
        └── test_api.py       # API endpoint tests                (Backend 3)
```

## Setup

You need two terminals: one for the backend, one for the frontend. Start the backend first.

### Backend (Python, uv)

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
cd backend
uv sync                            # creates .venv and installs everything (incl. pytest)

uv run uvicorn main:app --reload   # http://localhost:8000  (API docs: /docs)
uv run pytest                      # run tests
```

Adding a package: `uv add <package>` (or `uv add --dev <package>` for test-only tools), then commit `pyproject.toml` and `uv.lock`.

### Frontend (React, Vite)

Requires [Node.js](https://nodejs.org/) 18 or newer (comes with npm).

```bash
cd frontend
npm install                        # first time only (and after package.json changes)

npm run dev                        # http://localhost:5173
npm run build                      # production build into frontend/dist
```

Open **http://localhost:5173** in the browser. The frontend talks to the backend at `http://localhost:8000` (set in `src/services/api.js`), and the backend allows requests from port 5173 (CORS in `backend/main.py`). If you change either port, update both places.

Adding a package: `npm install <package>`, then commit `package.json` and `package-lock.json`.

## Shared interfaces (agree before coding — don't change without telling the team)

**Maze**: 2D list, `grid[row][col]`, `0` = walkable, `1` = wall.
**Position**: `(row, col)` tuple. Moves: up `(-1,0)`, down `(1,0)`, left `(0,-1)`, right `(0,1)`.

| Function | File | Signature | Returns |
|---|---|---|---|
| `is_valid` | `algorithms/utils.py` | `(grid, position)` | `bool` – inside grid and not a wall |
| `get_neighbors` | `algorithms/utils.py` | `(grid, position)` | `list[Position]` – valid neighbors |
| `reconstruct_path` | `algorithms/utils.py` | `(parent, start, goal)` | `list[Position]` – start→goal |
| `bfs` | `algorithms/bfs.py` | `(grid, start, goal)` | `SearchResult` |
| `dfs` | `algorithms/dfs.py` | `(grid, start, goal)` | `SearchResult` |
| `generate_maze` | `maze/generator.py` | `(rows=20, cols=20, wall_density=0.3)` | `(grid, start, goal)` |

`SearchResult` (dataclass in `algorithms/utils.py`) has two fields:

- `visited` = cells in the exact order they were explored (the frontend animates it).
- `path` = list of cells from start to goal.

**Every maze is solvable** – the generator guarantees a route, so there is no "goal not found" case to handle.

## API

| Method | Endpoint | Body / Query | Response |
|---|---|---|---|
| GET | `/api/health` | – | `{"status": "ok", ...}` |
| GET | `/api/maze/generate` | `?rows=&cols=&wall_density=` | `{grid, start, goal}` |
| POST | `/api/solve/bfs` | `{grid, start, goal}` | `{visited, path, visited_count, path_length, execution_time_ms}` |
| POST | `/api/solve/dfs` | `{grid, start, goal}` | same as BFS |

`path_length` = number of cells in `path`.

`/api/maze/generate` limits: `rows` and `cols` 2–100, `wall_density` 0–0.9 (defaults 20, 20, 0.3); out of range → `422`.
`/api/solve/*` returns `400` with `{"detail": "..."}` when the grid is empty/not rectangular/has values other than 0 and 1, when start or goal is outside the grid or on a wall, or when the maze can't be solved.

---

## Tasks

Each person works only in their own files. Work on your own branch (`backend-1/...`, `backend-2/...`, `backend-3/...`) and merge via pull request.

### 👤 Backend 1 — Graph utilities + BFS

Files: `algorithms/utils.py`, `algorithms/bfs.py`, `tests/test_bfs.py`

- [x] Implement `is_valid(grid, position)` – boundaries check + wall check
- [x] Implement `get_neighbors(grid, position)` – up/down/left/right using `DIRECTIONS` + `is_valid`
- [x] Implement `reconstruct_path(parent, start, goal)` – walk back from goal, reverse *(review with Backend 2)*
- [x] Implement `bfs(grid, start, goal)` with queue (`deque`), visited set, parent dict, visited-order list
- [x] BFS must return the **shortest** path
- [x] Write tests in `tests/test_bfs.py` (remove the skip marker): `is_valid`, `get_neighbors`, `reconstruct_path`, shortest path, start == goal
- [x] **Do first** – push `utils.py` early, Backend 2 depends on it

### 👤 Backend 2 — DFS + testing

Files: `algorithms/dfs.py`, `tests/test_dfs.py`

- [x] Implement `dfs(grid, start, goal)` with stack (list), visited set, parent dict, visited-order list
- [x] Use `get_neighbors` and `reconstruct_path` from `utils.py` (no duplicated neighbor logic)
- [x] `visited` must reflect the real exploration order (each cell only once)
- [x] Write tests in `tests/test_dfs.py`: path reaches goal, path is connected & avoids walls, no duplicate visits, start == goal
- [x] Review `reconstruct_path` together with Backend 1
- [x] Run the full test suite (`uv run pytest`) before each merge

### 👤 Backend 3 — FastAPI + maze generation

Files: `main.py`, `maze/generator.py`, `pyproject.toml`, `test_main.http`

- [x] Set up environment with uv: `pyproject.toml` + `uv.lock` (FastAPI, Uvicorn; dev: pytest, httpx), server runs with `--reload`
- [x] Implement `generate_maze(rows, cols, wall_density)`:
  - random walls ~30%
  - first row and last column always open (guarantees a route)
  - start = top-left `(0, 0)`, goal = bottom-right `(rows-1, cols-1)`
- [x] `GET /api/health` – return message that the server is running
- [x] `GET /api/maze/generate` – return grid, start, goal
- [x] `POST /api/solve/bfs` – run BFS, measure time (`time.perf_counter`), return visited, path, `visited_count`, `path_length`, `execution_time_ms`
- [x] `POST /api/solve/dfs` – same as BFS but with DFS
- [x] Configure CORS for the React dev server (confirm port with frontend)
- [x] Validate input (start/goal inside grid, grid not empty, start/goal not walls, maze solvable) – return 400 on bad input
- [x] Check everything works at `http://localhost:8000/docs` and with `test_main.http`
- [x] Tests: `tests/test_generator.py`, `tests/test_api.py`

## Suggested timeline (3 days)

| Day | Backend 1 | Backend 2 | Backend 3 |
|---|---|---|---|
| 1 | `utils.py` + tests | Write DFS tests against the agreed interface | Environment, health endpoint, `generator.py` |
| 2 | `bfs.py` + tests | `dfs.py` | Solve + generate endpoints, CORS |
| 3 | Bug fixes, help integration | Full test run, edge cases | Integration with frontend |
