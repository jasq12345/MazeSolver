import React from "react";
import "./Legend.css";

const ITEMS = [
  { cls: "empty", label: "Empty" },
  { cls: "wall", label: "Wall" },
  { cls: "start", label: "Start" },
  { cls: "goal", label: "Goal" },
  { cls: "visited", label: "Visited" },
  { cls: "path", label: "Path" },
];

export default function Legend() {
  return (
    <div className="legend">
      {ITEMS.map((item) => (
        <div className="legend-item" key={item.cls}>
          <span className={"legend-box " + item.cls} />
          {item.label}
        </div>
      ))}
    </div>
  );
}
