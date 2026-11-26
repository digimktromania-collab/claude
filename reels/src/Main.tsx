import React from "react";
import { AbsoluteFill, getInputProps, interpolate, useCurrentFrame } from "remotion";
import { Captions } from "./Captions";
import { Cuts } from "./Cuts";
import { FaceFog, faceAt } from "./FaceFog";
import { ACCENT, FPS, TL } from "./lib";
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

const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const p = frame / (TL.durationInFrames - 1);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, height: 10, width: `${p * 100}%`, background: ACCENT, boxShadow: `0 0 18px ${ACCENT}` }} />
  );
};

export const Main: React.FC = () => {
  const frame = useCurrentFrame();
  const zoom = useZoom();
  const [cx, cy] = faceAt(frame);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <AbsoluteFill
        style={{
          transform: `scale(${zoom})`,
          transformOrigin: `${cx}px ${cy}px`,
          filter: "contrast(1.07) saturate(1.12) brightness(1.02)",
        }}
      >
        <Cuts />
        {getInputProps().noFog ? null : <FaceFog />}
      </AbsoluteFill>
      {/* vignette */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 80% 70% at 50% 45%, transparent 60%, rgba(0,0,0,0.38) 100%)" }} />
      <Scenes />
      <Captions />
      <ProgressBar />
      <Sound />
    </AbsoluteFill>
  );
};
