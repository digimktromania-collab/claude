import React from "react";
import { Audio } from "@remotion/media";
import { interpolate, Sequence, staticFile } from "remotion";
import { FPS, TL } from "./lib";

/**
 * Gains relative to the voice (normalised to -14 LUFS), from each file's measured peak loudness.
 * Utility sounds sit 18 dB under the voice; the signature moments (Claude Apps sting,
 * notification, success) sit 14 dB under so they read clearly; typing sits ~24 dB under.
 */
const SFX_GAIN: Record<string, number> = {
  whoosh: 0.11,
  pop: 0.076,
  click: 0.219,
  ding: 0.075,
  riser: 0.126,
  sting: 0.15,
  success: 0.13,
  notify: 0.13,
  mouseclick: 0.28,
  send: 0.122,
  typing: 0.19,
};
const MUSIC_DUCKED = 0.083; // -28 dB vs voice
const MUSIC_OPEN = 0.21; // -20 dB vs voice (only in gaps)

const speech = TL.speech as [number, number][];
const distToSpeech = (t: number) => {
  let d = Infinity;
  for (const [s, e] of speech) {
    if (t >= s && t <= e) return 0;
    d = Math.min(d, Math.abs(t - s), Math.abs(t - e));
  }
  return d;
};

type Sfx = { t: number; type: string; dur: number };

export const Sound: React.FC = () => {
  const total = TL.durationInFrames;
  return (
    <>
      <Audio
        name="Lo-fi music"
        src={staticFile("sfx/lofi.wav")}
        loop
        loopVolumeCurveBehavior="extend"
        volume={(fr) => {
          const t = fr / FPS;
          const duck = interpolate(distToSpeech(t), [0.05, 0.35], [MUSIC_DUCKED, MUSIC_OPEN], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const fade = interpolate(fr, [0, 12, total - 45, total], [0, 1, 1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return duck * fade;
        }}
      />
      {(TL.sfx as Sfx[]).map((e, i) => {
        const looped = e.dur > 0;
        const frames = looped ? Math.max(1, Math.round(e.dur * FPS)) : 50;
        return (
          <Sequence key={i} name={`SFX ${e.type}`} from={Math.round(e.t * FPS)} durationInFrames={frames}>
            <Audio
              src={staticFile(`sfx/${e.type}.wav`)}
              loop={looped}
              volume={(fr) =>
                looped
                  ? SFX_GAIN[e.type] * interpolate(fr, [0, 3, frames - 4, frames], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
                  : SFX_GAIN[e.type]
              }
            />
          </Sequence>
        );
      })}
    </>
  );
};
