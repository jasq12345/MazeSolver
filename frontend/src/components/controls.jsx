import React from 'react';
import './controls.css';

export default function Controls({
  algorithm,
  onAlgorithmChange,
  onGenerate,
  onSolve,
  onClear,
  isLoading,
  isAnimating,
}) {
  return (
    <div className="controls">
      <div className="control-group">
        <label>Algorithm: </label>
        <select 
          value={algorithm} 
          onChange={(e) => onAlgorithmChange(e.target.value)}
          disabled={isLoading || isAnimating}
        >
          <option value="BFS">BFS</option>
          <option value="DFS">DFS</option>
        </select>
      </div>

      <div className="buttons">
        <button onClick={onGenerate} disabled={isLoading || isAnimating}>
          Generate Maze
        </button>
        <button onClick={onSolve} disabled={isLoading || isAnimating}>
          {isLoading ? 'Solving...' : 'Solve'}
        </button>
        <button onClick={onClear} disabled={isLoading}>
          Clear Solution
        </button>
      </div>
    </div>
  );
}