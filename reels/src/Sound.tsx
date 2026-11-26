import React from "react";
import { Audio } from "@remotion/media";
import { interpolate, Sequence, staticFile } from "remotion";
import { FPS, TL } from "./lib";

/**
 * Gains are relative to the voice (normalised to -14 LUFS).
 * SFX: measured peak loudness of each file, scaled to sit 18 dB under the voice peaks.
 * Music: -28 dB under the voice while she speaks, opens up to -20 dB in gaps (ducking).
 */
const SFX_GAIN: Record<string, number> = {
  whoosh: 0.143,
  pop: 0.076,
  click: 0.219,
  ding: 0.075,
  riser: 0.126,
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
      {TL.sfx.map((e, i) => (
        <Sequence key={i} name={`SFX ${e.type}`} from={Math.round(e.t * FPS)} durationInFrames={e.type === "riser" ? 40 : 45}>
          <Audio src={staticFile(`sfx/${e.type}.wav`)} volume={SFX_GAIN[e.type]} />
        </Sequence>
      ))}
    </>
  );
};
