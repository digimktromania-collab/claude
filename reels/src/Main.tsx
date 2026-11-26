import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Captions } from "./Captions";
import { Cuts } from "./Cuts";
import { FullGraphics, PanelGraphics } from "./Graphics";
import { faceAt, PANEL_H, splitOffset, splitProgress, zoomAt } from "./layout";
import { ACCENT, TL } from "./lib";
import { Sound } from "./Sound";

const PAPER_BG = "#F4F0E8";

const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const p = frame / (TL.durationInFrames - 1);
  return <div style={{ position: "absolute", left: 0, top: 0, height: 10, width: `${p * 100}%`, background: ACCENT }} />;
};

export const Main: React.FC = () => {
  const frame = useCurrentFrame();
  const p = splitProgress(frame);
  const [cx, cy] = faceAt(frame);
  const zoom = 1 + (zoomAt(frame) - 1) * (1 - p);
  const ty = splitOffset(frame) * p;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* the footage: full screen, or pushed down into the lower window */}
      <AbsoluteFill
        style={{
          transform: `translateY(${ty}px) scale(${zoom})`,
          transformOrigin: `${cx}px ${cy}px`,
          filter: "contrast(1.06) saturate(1.1) brightness(1.02)",
        }}
      >
        <Cuts />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 85% 70% at 50% 45%, transparent 62%, rgba(0,0,0,0.32) 100%)" }} />

      {/* graphics for full-screen moments: only above the head or on the chest */}
      <FullGraphics />

      {/* graphics panel (split screen) slides down from the top */}
      <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: PANEL_H, transform: `translateY(${(p - 1) * (PANEL_H + 20)}px)` }}>
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: PAPER_BG,
            backgroundImage: "radial-gradient(rgba(31,30,29,0.10) 2px, transparent 2px)",
            backgroundSize: "34px 34px",
            boxShadow: "0 18px 40px rgba(0,0,0,0.35)",
            overflow: "hidden",
          }}
        >
          <PanelGraphics />
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: -8, height: 8, background: ACCENT }} />
      </div>

      <Captions />
      <ProgressBar />
      <Sound />
    </AbsoluteFill>
  );
};
