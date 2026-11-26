import React from "react";
import { ACCENT } from "./lib";

/** Claude-style spark mark (drawn, no external asset). */
export const ClaudeMark: React.FC<{ size: number; color?: string; rotate?: number }> = ({
  size,
  color = ACCENT,
  rotate = 0,
}) => {
  const rays = 12;
  return (
    <svg width={size} height={size} viewBox="-50 -50 100 100" style={{ transform: `rotate(${rotate}deg)` }}>
      {new Array(rays).fill(0).map((_, i) => (
        <rect
          key={i}
          x={-4.2}
          y={-47}
          width={8.4}
          height={i % 2 === 0 ? 47 : 38}
          rx={4.2}
          fill={color}
          transform={`rotate(${(360 / rays) * i + (i % 3) * 4})`}
        />
      ))}
      <circle r={9} fill={color} />
    </svg>
  );
};

export const AppleLogo: React.FC<{ size: number; color?: string }> = ({ size, color = "#111" }) => (
  <svg width={size} height={size} viewBox="0 0 100 110">
    <defs>
      <mask id="bite">
        <rect width="100" height="110" fill="#fff" />
        <circle cx="96" cy="52" r="17" fill="#000" />
      </mask>
    </defs>
    <g mask="url(#bite)" fill={color}>
      <circle cx="34" cy="62" r="30" />
      <circle cx="66" cy="62" r="30" />
      <ellipse cx="50" cy="80" rx="38" ry="28" />
      <circle cx="38" cy="96" r="12" />
      <circle cx="62" cy="96" r="12" />
    </g>
    <circle cx="50" cy="36" r="9" fill="#fff" opacity={0} />
    <ellipse cx="58" cy="16" rx="9" ry="16" transform="rotate(40 58 16)" fill={color} />
  </svg>
);

export const WindowsLogo: React.FC<{ size: number; color?: string }> = ({ size, color = "#0A74DA" }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <rect x="4" y="4" width="44" height="44" fill={color} />
    <rect x="52" y="4" width="44" height="44" fill={color} />
    <rect x="4" y="52" width="44" height="44" fill={color} />
    <rect x="52" y="52" width="44" height="44" fill={color} />
  </svg>
);
