import React, { useState, useRef, useEffect } from "react";
import MazeGrid from "./components/MazeGrid";
import Legend from "./components/Legend";
import Controls from "./components/Controls";
import Statistics from "./components/Statistics";
import { getRandomMaze, solveBFS, solveDFS } from "./services/api";

const ROWS = 15;
const COLS = 25;
const ANIMATION_DELAY = 30; // ms between revealed cells

// Demo maze shown before the first "Generate Maze" click
function createDemoMaze() {
  return Array.from({ length: ROWS }, () =>
    Array.from({ length: COLS }, () => (Math.random() < 0.25 ? 1 : 0))
  );
}

export default function App() {
  const [maze, setMaze] = useState(createDemoMaze);
  const [start, setStart] = useState([0, 0]);
  const [goal, setGoal] = useState([ROWS - 1, COLS - 1]);
  const [algorithm, setAlgorithm] = useState("BFS");
  const [visited, setVisited] = useState([]);
  const [path, setPath] = useState([]);
  const [result, setResult] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  const timerRef = useRef(null);

  // Stop the animation if the page is closed
  useEffect(() => () => clearInterval(timerRef.current), []);

  // Remove visited cells, path and statistics (the maze stays the same)
  function clearSolution() {
    clearInterval(timerRef.current);
    setIsAnimating(false);
    setVisited([]);
    setPath([]);
    setResult(null);
    setMessage("");
  }

  // Click on a cell: empty -> wall, wall -> empty
  function handleCellClick(r, c) {
    clearSolution(); // editing clears previous algorithm results
    setMaze((old) =>
      old.map((row, i) => row.map((cell, j) => (i === r && j === c ? 1 - cell : cell)))
    );
  }

  // Generate Maze: get a new maze from the backend
  async function handleGenerate() {
    clearSolution();
    setIsLoading(true);
    try {
      const data = await getRandomMaze();
      const grid = Array.isArray(data) ? data : data.grid;
      setMaze(grid);
      setStart(data.start || [0, 0]);
      setGoal(data.goal || [grid.length - 1, grid[0].length - 1]);
    } catch (error) {
      setMessage("Could not connect to the backend. Please try again.");
    }
    setIsLoading(false);
  }

  // Solve: send the maze to the backend, then animate the result
  async function handleSolve() {
    clearSolution();
    setIsLoading(true);
    try {
      const solver = algorithm === "BFS" ? solveBFS : solveDFS;
      const data = await solver(maze, start, goal);
      setIsLoading(false);
      animate(data);
    } catch (error) {
      setIsLoading(false);
      // fetch() throws TypeError when the server is unreachable;
      // otherwise the backend answered with an error (400 = no route to the goal)
      if (error instanceof TypeError) {
        setMessage("Could not connect to the backend. Please try again.");
      } else {
        setMessage("No path found.");
      }
    }
  }

  // Reveal visited cells one by one, then show the final path
  function animate(data) {
    const cells = data.visited || [];
    let i = 0;
    setIsAnimating(true);

    timerRef.current = setInterval(() => {
      i++;
      setVisited(cells.slice(0, i));

      if (i >= cells.length) {
        clearInterval(timerRef.current);
        // the backend does not send "found": a non-empty path means a route exists
        const found = data.found ?? (data.path || []).length > 0;
        if (found) {
          setPath(data.path);
        } else {
          setMessage("No path found.");
        }
        setResult({ ...data, found });
        setIsAnimating(false);
      }
    }, ANIMATION_DELAY);
  }

  function handleClear() {
    clearSolution();
  }

  return (
    <div className="page">
      <header className="header">
        <h1>Maze Solver</h1>
        <p>Click on cells to build walls, then let BFS or DFS find the way out.</p>
      </header>

      <main className="layout">
        <aside className="side-panel">
          <div className="card">
            <h2>Controls</h2>
            <Controls
              algorithm={algorithm}
              onAlgorithmChange={setAlgorithm}
              onGenerate={handleGenerate}
              onSolve={handleSolve}
              onClear={handleClear}
              isLoading={isLoading}
              isAnimating={isAnimating}
            />
            {message && (
              <p style={{ color: "#c92a2a", fontWeight: "bold", margin: "10px 0 0", fontSize: "14px", textAlign: "center"}}>
                {message}
              </p>
            )}
          </div>

          <div className="card">
            <Statistics algorithm={algorithm} result={result} />
          </div>
        </aside>

        <section className="card maze-card">
          <MazeGrid
            maze={maze}
            start={start}
            goal={goal}
            visited={visited}
            path={path}
            onCellClick={handleCellClick}
            disabled={isAnimating || isLoading}
          />
          <Legend />
        </section>
      </main>
    </div>
  );
}
