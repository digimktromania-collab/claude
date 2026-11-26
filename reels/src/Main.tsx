import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Captions } from "./Captions";
import { Cuts } from "./Cuts";
import { FPS, TL } from "./lib";
import { Scenes } from "./Scenes";
import { Sound } from "./Sound";

/** Punch-in zoom: 106% / 110% alternating on important phrases, snapping in over 3 frames. */
const useZoom = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const z = TL.zooms.find((p) => t >= p.start && t < p.end);
  if (!z) return 1;
  const sinceIn = (t - z.start) * FPS;
  const untilOut = (z.end - t) * FPS;
  const k = Math.min(
    interpolate(sinceIn, [0, 3], [0, 1], { extrapolateRight: "clamp" }),
    interpolate(untilOut, [0, 3], [0, 1], { extrapolateRight: "clamp" }),
  );
  // slow creep while the phrase lasts keeps it alive
  const creep = 1 + 0.008 * Math.min(1, sinceIn / 60);
  return (1 + (z.scale - 1) * k) * creep;
};

export const Main: React.FC = () => {
  const zoom = useZoom();
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${zoom})`, transformOrigin: "50% 38%" }}>
        <Cuts />
      </AbsoluteFill>
      <Scenes />
      <Captions />
      <Sound />
    </AbsoluteFill>
  );
};
