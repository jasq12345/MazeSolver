# Maze Solver

A web app that shows how graph search algorithms find their way through a maze.

Generate a random maze (or draw walls yourself), pick an algorithm and watch it explore the grid cell by cell until it reaches the goal. Afterwards you can compare algorithms by how many cells they visited, how long the found path is and how fast they ran.

The maze is treated as a **graph**: every walkable cell is a vertex, and neighboring cells (up, down, left, right) are connected by an edge.

## Algorithms

| Algorithm | Data structure | Shortest path? | Status |
|---|---|---|---|
| BFS – Breadth-First Search | queue | ✅ yes | ✅ done |
| DFS – Depth-First Search | stack | ❌ no | ✅ done |
| Dijkstra | priority queue | ✅ yes | ✅ done |
| A* | priority queue + heuristic | ✅ yes | ✅ done |

## Tech stack

| Part | Technology |
|---|---|
| Frontend | React 18 + Vite 8 |
| Backend | Python 3.12, FastAPI, Uvicorn |
| Tooling | uv (Python packages), npm (JS packages), pytest |

## How it works

```
Browser (React, :5173)
      │  HTTP / JSON
      ▼
Backend (FastAPI, :8000)
      ├── generates random mazes
      ├── runs the chosen algorithm
      └── returns visited cells (in order) · final path · statistics
      │
      ▼
Browser animates the exploration and draws the path
```

## Project structure

```
MazeSolver/
├── README.md                 # this file – project overview + setup
├── frontend/                 # React + Vite app
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx          # entry point
│       ├── App.jsx
│       ├── components/       # MazeGrid, Controls, Statistics, Legend
│       └── services/api.js   # calls the backend
└── backend/                  # FastAPI app + algorithms
    └── README.md             # backend details, API, team tasks
```

➡️ Backend details (code structure, API, how to add an algorithm, current tasks): **[backend/README.md](backend/README.md)**

## Setup

### Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) – installs Python and backend packages for you
- [Node.js](https://nodejs.org/) 20.19+ or 22.12+ (comes with npm) – needed by Vite 8
- Git

### 1. Clone

```bash
git clone git@github.com:jasq12345/MazeSolver.git
cd MazeSolver
```

### 2. Start the backend (terminal 1)

```bash
cd backend
uv sync                            # first time: creates .venv and installs packages
uv run uvicorn main:app --reload   # http://localhost:8000  (API docs: /docs)
```

### 3. Start the frontend (terminal 2)

```bash
cd frontend
npm install                        # first time (and after package.json changes)
npm run dev                        # http://localhost:5173
```

### 4. Open the app

Go to **http://localhost:5173**.

The frontend calls the backend at `http://localhost:8000` (`frontend/src/services/api.js`), and the backend only accepts browser requests from port 5173 (CORS in `backend/main.py`). If you change a port, update both places.

### Running tests

```bash
cd backend
uv run pytest
```

### Production build of the frontend

```bash
cd frontend
npm run build                      # output in frontend/dist
```

## Working together

- One branch per task, merged into `main` through a pull request.
- Each person owns their own files (see [backend/README.md](backend/README.md#tasks)), so nobody edits the same file at the same time.
- Run `uv run pytest` before opening a pull request.
- Adding packages: backend `uv add <pkg>` (commit `pyproject.toml` + `uv.lock`), frontend `npm install <pkg>` (commit `package.json` + `package-lock.json`).
