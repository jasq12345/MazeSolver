"""FastAPI app - API layer between the React frontend and the algorithms.

Owner: Backend 3

Run (from backend/):  uvicorn main:app --reload
Docs:                 http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Maze Solver API")

# TODO (Backend 3): confirm the React dev server URL with the frontend team.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class MazeRequest(BaseModel):
    grid: list[list[int]]   # 0 = walkable, 1 = wall
    start: tuple[int, int]  # (row, col)
    goal: tuple[int, int]   # (row, col)


class SolveResponse(BaseModel):
    visited: list[tuple[int, int]]  # exploration order
    path: list[tuple[int, int]]     # start -> goal (maze is always solvable)
    visited_count: int
    path_length: int                # number of cells in path
    execution_time_ms: float


class MazeResponse(BaseModel):
    grid: list[list[int]]
    start: tuple[int, int]
    goal: tuple[int, int]


@app.get("/api/health")
def health():
    """TODO (Backend 3): return a simple message confirming the server is running."""
    raise NotImplementedError


@app.post("/api/solve/bfs", response_model=SolveResponse)
def solve_bfs(request: MazeRequest):
    """TODO (Backend 3):
      1. Receive the maze request.
      2. Run bfs() and measure execution time (time.perf_counter).
      3. Compute visited_count and path_length.
      4. Return SolveResponse.
    """
    raise NotImplementedError


@app.post("/api/solve/dfs", response_model=SolveResponse)
def solve_dfs(request: MazeRequest):
    """TODO (Backend 3): same as solve_bfs but runs dfs()."""
    raise NotImplementedError


@app.get("/api/maze/generate", response_model=MazeResponse)
def generate(rows: int = 20, cols: int = 20, wall_density: float = 0.3):
    """TODO (Backend 3): call generate_maze() and return grid, start, goal."""
    raise NotImplementedError
