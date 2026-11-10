import React from "react";
import "./MazeGrid.css";

export default function MazeGrid({
  maze,
  start,
  goal,
  visited = [],
  path = [],
  onCellClick,
  disabled = false,
}) {
  const key = (r, c) => r + "," + c;
  const visitedSet = new Set(visited.map(([r, c]) => key(r, c)));
  const pathSet = new Set(path.map(([r, c]) => key(r, c)));

  const isStart = (r, c) => r === start[0] && c === start[1];
  const isGoal = (r, c) => r === goal[0] && c === goal[1];

  function getCellClass(r, c) {
    if (isStart(r, c)) return "cell start";
    if (isGoal(r, c)) return "cell goal";
    if (maze[r][c] === 1) return "cell wall";
    if (pathSet.has(key(r, c))) return "cell path";
    if (visitedSet.has(key(r, c))) return "cell visited";
    return "cell empty";
  }

  function handleClick(r, c) {
    if (disabled) return;
    if (isStart(r, c) || isGoal(r, c)) return;
    onCellClick(r, c);
  }

  return (
    <div
      className={disabled ? "maze-grid disabled" : "maze-grid"}
      style={{ gridTemplateColumns: `repeat(${maze[0].length}, var(--cell-size))` }}
    >
      {maze.map((row, r) =>
        row.map((_, c) => (
          <div
            key={key(r, c)}
            className={getCellClass(r, c)}
            onClick={() => handleClick(r, c)}
          />
        ))
      )}
    </div>
  );
}
