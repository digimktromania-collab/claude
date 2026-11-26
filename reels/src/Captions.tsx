import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ACCENT, SANS, SERIF, TL } from "./lib";

type Word = { text: string; start: number; end: number; key: boolean };

const OUTLINE =
  "0 0 2px #000, 0 4px 0 rgba(0,0,0,0.85), 0 6px 22px rgba(0,0,0,0.55)";

/** 3–4 words per page, bold, lower third; spoken word in accent, keywords in italic serif. */
export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const page = TL.captions.find((c) => t >= c.start && t < c.end);
  // the outro has its own kinetic typography
  if (!page || t >= TL.scenes.outro.start) return null;

  const pageIn = spring({
    frame: frame - Math.round(page.start * fps),
    fps,
    config: { damping: 15, stiffness: 260 },
    durationInFrames: 7,
  });

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: 70,
          right: 70,
          top: 1370,
          height: 300,
          display: "flex",
          flexWrap: "wrap",
          alignContent: "center",
          justifyContent: "center",
          columnGap: 22,
          rowGap: 0,
          transform: `translateY(${(1 - pageIn) * 30}px) scale(${0.9 + 0.1 * pageIn})`,
          opacity: pageIn,
        }}
      >
        {(page.words as Word[]).map((w, i, arr) => {
          // exactly one highlighted word: the latest word that has started
          const lastStarted = arr.reduce((acc, x, j) => (t >= x.start ? j : acc), -1);
          const active = i === lastStarted && t < w.end + 0.25;
          const spoken = t >= w.start;
          const pop = active
            ? interpolate(t - w.start, [0, 0.08, 0.2], [1, 1.12, 1.06], {
                extrapolateRight: "clamp",
              })
            : 1;
          return (
            <span
              key={i}
              style={{
                fontFamily: w.key ? SERIF : SANS,
                fontStyle: w.key ? "italic" : "normal",
                fontWeight: w.key ? 400 : 900,
                fontSize: w.key ? 112 : 88,
                lineHeight: 1.12,
                letterSpacing: w.key ? 0 : -1.5,
                color: active ? ACCENT : "#FFFFFF",
                opacity: spoken ? 1 : 0.88,
                textShadow: OUTLINE,
                transform: `scale(${pop})`,
                display: "inline-block",
                padding: w.key ? "0 10px 0 4px" : 0,
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
