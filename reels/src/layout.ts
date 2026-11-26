import { Easing, interpolate } from "remotion";
import { f, FPS, TL } from "./lib";

/** Height of the graphics panel in split-screen mode. Her face always stays below it. */
export const PANEL_H = 900;
const TRANSITION = 10; // frames

type Mode = { mode: string; start: number; end: number };
const modes = TL.modes as Mode[];

/** 0 = full-screen talking head, 1 = split screen (graphics on top, face below) */
export const splitProgress = (frame: number) => {
  const t = frame / FPS;
  let idx = modes.findIndex((m) => t >= m.start && t < m.end);
  if (idx === -1) idx = modes.length - 1;
  const target = modes[idx].mode === "split" ? 1 : 0;
  if (idx === 0) return target;
  const prev = modes[idx - 1].mode === "split" ? 1 : 0;
  return interpolate(frame - f(modes[idx].start), [0, TRANSITION], [prev, target], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
};

const boxes = TL.faceBox as [number, number, number, number][];
export const faceAt = (frame: number) => boxes[Math.max(0, Math.min(boxes.length - 1, frame))];

/** vertical offset that puts her face in the lower window during split screen */
export const splitOffset = (frame: number) => {
  const [, cy] = faceAt(frame);
  const windowCenter = PANEL_H + (1920 - PANEL_H) * 0.44;
  return Math.max(0, Math.min(PANEL_H, windowCenter - cy));
};

/** punch-in zoom for full-screen sentences (alternating 106% / 110%) */
export const zoomAt = (frame: number) => {
  const t = frame / FPS;
  const z = TL.zooms.find((p) => t >= p.start && t < p.end);
  if (!z) return 1;
  const k = Math.min(
    interpolate((t - z.start) * FPS, [0, 3], [0, 1], { extrapolateRight: "clamp" }),
    interpolate((z.end - t) * FPS, [0, 3], [0, 1], { extrapolateRight: "clamp" }),
  );
  return 1 + (z.scale - 1) * k;
};
