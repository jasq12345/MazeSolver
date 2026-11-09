import React from 'react';
import './statistics.css';

export default function Statistics({ algorithm, result }) {
  if (!result) {
    return (
      <div className="statistics">
        <h3>Statistics</h3>
        <p>No search executed yet.</p>
      </div>
    );
  }

  return (
    <div className="statistics">
      <h3>Statistics</h3>
      <p><strong>Algorithm:</strong> {algorithm}</p>
      <p><strong>Path found:</strong> {result.found ? 'Yes' : 'No'}</p>
      <p><strong>Visited cells:</strong> {result.visited_count}</p>
      <p><strong>Path length:</strong> {result.path_length}</p>
      <p><strong>Execution time:</strong> {result.execution_time_ms} ms</p>
    </div>
  );
}