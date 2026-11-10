"""FastAPI app - API layer between the React frontend and the algorithms.

Owner: Backend 3

Run (from backend/):  uvicorn main:app --reload
Docs:                 http://localhost:8000/docs
"""

import time
from collections.abc import Callable

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from algorithms.astar import astar
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.utils import OPEN, WALL, Grid, Position, SearchResult
from maze.generator import generate_maze

app = FastAPI(title="Maze Solver API")

# React dev servers: Vite (5173) and Create React App (3000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
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


def validate_maze(grid: Grid, start: Position, goal: Position) -> None:
    """Raise HTTP 400 if the maze or positions don't make sense."""
    if not grid or not grid[0]:
        raise HTTPException(400, "grid must not be empty")

    cols = len(grid[0])
    if any(len(row) != cols for row in grid):
        raise HTTPException(400, "all grid rows must have the same length")
    if any(cell not in (OPEN, WALL) for row in grid for cell in row):
        raise HTTPException(400, "grid cells must be 0 (open) or 1 (wall)")

    for name, (row, col) in (("start", start), ("goal", goal)):
        if not (0 <= row < len(grid) and 0 <= col < cols):
            raise HTTPException(400, f"{name} {(row, col)} is outside the grid")
        if grid[row][col] == WALL:
            raise HTTPException(400, f"{name} {(row, col)} is a wall")


def solve(
    request: MazeRequest, algorithm: Callable[[Grid, Position, Position], SearchResult]
) -> SolveResponse:
    """Validate the request, run `algorithm`, time it and build the response."""
    start, goal = tuple(request.start), tuple(request.goal)
    validate_maze(request.grid, start, goal)

    started = time.perf_counter()
    result = algorithm(request.grid, start, goal)
    elapsed_ms = (time.perf_counter() - started) * 1000

    # Generated mazes are always solvable, but a hand-made grid sent to the API might not be.
    if not result.path or result.path[0] != start:
        raise HTTPException(400, "maze is not solvable: goal cannot be reached from start")

    return SolveResponse(
        visited=result.visited,
        path=result.path,
        visited_count=len(result.visited),
        path_length=len(result.path),
        execution_time_ms=round(elapsed_ms, 3),
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Maze Solver backend is running"}


@app.post("/api/solve/bfs", response_model=SolveResponse)
def solve_bfs(request: MazeRequest):
    return solve(request, bfs)


@app.post("/api/solve/dfs", response_model=SolveResponse)
def solve_dfs(request: MazeRequest):
    return solve(request, dfs)


@app.post("/api/solve/dijkstra", response_model=SolveResponse)
def solve_dijkstra(request: MazeRequest):
    return solve(request, dijkstra)


@app.post("/api/solve/astar", response_model=SolveResponse)
def solve_astar(request: MazeRequest):
    return solve(request, astar)


@app.get("/api/maze/generate", response_model=MazeResponse)
def generate(
    rows: int = Query(20, ge=2, le=100),
    cols: int = Query(20, ge=2, le=100),
    wall_density: float = Query(0.3, ge=0, le=0.9),
):
    grid, start, goal = generate_maze(rows, cols, wall_density)
    return MazeResponse(grid=grid, start=start, goal=goal)
