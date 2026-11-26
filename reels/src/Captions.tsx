import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { PANEL_H, splitProgress } from "./layout";
import { ACCENT, INK, SANS, SERIF, TL } from "./lib";

type Word = { text: string; start: number; end: number; key: boolean };

const OUTLINE = "0 0 2px #000, 0 4px 0 rgba(0,0,0,0.85), 0 6px 22px rgba(0,0,0,0.55)";

/**
 * 3–4 words per page. Full screen: white, lower third (on the chest).
 * Split screen: dark ink at the bottom of the graphics panel, never on the face.
 */
export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const page = TL.captions.find((c) => t >= c.start && t < c.end);
  if (!page || t >= TL.scenes.outro.start) return null;

  const p = splitProgress(frame);
  const split = p > 0.5;
  const pageIn = spring({ frame: frame - Math.round(page.start * fps), fps, config: { damping: 15, stiffness: 260 }, durationInFrames: 7 });
  // in split mode the captions ride with the panel's bottom edge
  const panelBottom = PANEL_H + (p - 1) * (PANEL_H + 20);
  const top = split ? panelBottom - 175 : 1390;
  const words = page.words as Word[];
  const lastStarted = words.reduce((acc, x, j) => (t >= x.start ? j : acc), -1);

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: 60,
          right: 60,
          top,
          height: split ? 150 : 280,
          display: "flex",
          flexWrap: "wrap",
          alignContent: "center",
          justifyContent: "center",
          columnGap: 18,
          transform: `translateY(${(1 - pageIn) * 24}px)`,
          // fade out while the layout is switching so text never crosses her face
          opacity: pageIn * (p < 0.04 || p > 0.97 ? 1 : 0),
        }}
      >
        {words.map((w, i) => {
          const active = i === lastStarted && t < w.end + 0.25;
          const pop = active ? interpolate(t - w.start, [0, 0.08, 0.2], [1, 1.1, 1.05], { extrapolateRight: "clamp" }) : 1;
          const base = split ? 66 : 86;
          return (
            <span
              key={i}
              style={{
                fontFamily: w.key ? SERIF : SANS,
                fontStyle: w.key ? "italic" : "normal",
                fontWeight: w.key ? 400 : 900,
                fontSize: w.key ? base * 1.25 : base,
                lineHeight: 1.12,
                letterSpacing: w.key ? 0 : -1.2,
                color: active ? ACCENT : split ? INK : "#fff",
                textShadow: split ? "none" : OUTLINE,
                transform: `scale(${pop})`,
                display: "inline-block",
                padding: w.key ? "0 8px 0 2px" : 0,
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
