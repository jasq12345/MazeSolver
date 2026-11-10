const API_BASE_URL = 'http://localhost:8000';

export async function checkBackend() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
}

export async function getRandomMaze() {
  const response = await fetch(`${API_BASE_URL}/api/maze/generate`);
  if (!response.ok) throw new Error('Failed to generate maze');
  return response.json();
}

export async function solveBFS(grid, start, goal) {
  const response = await fetch(`${API_BASE_URL}/api/solve/bfs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ grid, start, goal }),
  });
  if (!response.ok) throw new Error('Failed to solve with BFS');
  return response.json();
}

export async function solveDFS(grid, start, goal) {
  const response = await fetch(`http://localhost:8000/api/solve/dfs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ grid, start, goal }),
  });
  if (!response.ok) throw new Error('Failed to solve with DFS');
  return response.json();
}
