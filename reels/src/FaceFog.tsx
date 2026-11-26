import React from "react";
import { AbsoluteFill, interpolate, Sequence, useCurrentFrame } from "remotion";
import { Cuts } from "./Cuts";
import { f, TL } from "./lib";

const boxes = TL.faceBox as [number, number, number, number][];
export const faceAt = (frame: number) => boxes[Math.max(0, Math.min(boxes.length - 1, frame))];

/** Blurred, slightly hazy copy of the footage, masked to the tracked face. `frame` is absolute. */
const Fog: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame(); // absolute (parent offsets cancel out)
  const [cx, cy, w, h] = faceAt(frame);
  const a = f(start);
  const b = f(end);
  const k = interpolate(frame, [a, a + 6, b - 6, b], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const mask = `radial-gradient(ellipse ${w * 0.72}px ${h * 0.92}px at ${cx}px ${cy - h * 0.04}px, #000 58%, transparent 100%)`;
  return (
    <AbsoluteFill style={{ opacity: k, WebkitMaskImage: mask, maskImage: mask }}>
      <AbsoluteFill style={{ filter: "blur(26px) brightness(1.08) saturate(0.9)" }}>
        <Cuts muted />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "rgba(255,255,255,0.14)" }} />
    </AbsoluteFill>
  );
};

/** "Fog" over the face where lip-sync was measured to be off. */
export const FaceFog: React.FC = () => {
  return (
    <>
      {(TL.fog as [number, number][]).map(([s, e], i) => (
        <Sequence key={i} name={`Ceață față ${i + 1}`} from={f(s)} durationInFrames={f(e) - f(s)}>
          <Sequence from={-f(s)}>
            <Fog start={s} end={e} />
          </Sequence>
        </Sequence>
      ))}
    </>
  );
};
