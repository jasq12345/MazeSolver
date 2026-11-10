"""Tests for the FastAPI endpoints.  Owner: Backend 3"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

MAZE = {
    "grid": [
        [0, 0, 1, 0, 0],
        [1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ],
    "start": [0, 0],
    "goal": [2, 2],
}


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_default():
    data = client.get("/api/maze/generate").json()
    assert len(data["grid"]) == 20 and len(data["grid"][0]) == 20
    assert data["start"] == [0, 0]
    assert data["goal"] == [19, 19]


def test_generate_custom_size():
    data = client.get("/api/maze/generate?rows=7&cols=9&wall_density=0.2").json()
    assert len(data["grid"]) == 7 and len(data["grid"][0]) == 9
    assert data["goal"] == [6, 8]


def test_generate_rejects_bad_size():
    assert client.get("/api/maze/generate?rows=1000").status_code == 422


@pytest.mark.parametrize("algorithm", ["bfs", "dfs", "dijkstra", "astar"])
def test_solve_response_shape(algorithm):
    response = client.post(f"/api/solve/{algorithm}", json=MAZE)
    assert response.status_code == 200
    data = response.json()
    assert data["path"][0] == [0, 0]
    assert data["path"][-1] == [2, 2]
    assert data["visited_count"] == len(data["visited"])
    assert data["path_length"] == len(data["path"])
    assert data["execution_time_ms"] >= 0


def test_bfs_returns_shortest_path():
    data = client.post("/api/solve/bfs", json=MAZE).json()
    assert data["path"] == [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2]]


@pytest.mark.parametrize("algorithm", ["bfs", "dfs", "dijkstra", "astar"])
def test_solve_generated_maze(algorithm):
    maze = client.get("/api/maze/generate?rows=15&cols=15").json()
    response = client.post(f"/api/solve/{algorithm}", json=maze)
    assert response.status_code == 200
    assert response.json()["path"][-1] == maze["goal"]


@pytest.mark.parametrize(
    "body",
    [
        {**MAZE, "grid": []},                          # empty grid
        {**MAZE, "grid": [[0, 0], [0]]},               # rows of different length
        {**MAZE, "grid": [[0, 2], [0, 0]], "goal": [1, 1]},  # invalid cell value
        {**MAZE, "start": [-1, 0]},                    # start outside grid
        {**MAZE, "goal": [9, 9]},                      # goal outside grid
        {**MAZE, "goal": [0, 2]},                      # goal is a wall
        {"grid": [[0, 1], [1, 0]], "start": [0, 0], "goal": [1, 1]},  # unsolvable
    ],
)
@pytest.mark.parametrize("algorithm", ["bfs", "dfs", "dijkstra", "astar"])
def test_solve_rejects_bad_input(algorithm, body):
    assert client.post(f"/api/solve/{algorithm}", json=body).status_code == 400
