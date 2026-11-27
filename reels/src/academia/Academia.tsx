import React from "react";
import { Audio } from "@remotion/media";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ClaudeMark } from "../Logos";
import { ACCENT, INK, PAPER, SANS, SERIF } from "../lib";
import { BaseCuts, PersonCuts } from "./Cuts";
import D from "./data.json";

const FPS = D.fps;
const E = D.events;
const f = (s: number) => Math.round(s * FPS);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const PINK_A = "#F6DCDC";
const PINK_B = "#E9B9C0";
const shadow = "0 30px 70px rgba(0,0,0,0.35), 0 8px 20px rgba(0,0,0,0.2)";

/* ---------------------------------------------------------- geometry */
/** person slides down a little when the trees appear, to make room for them (edges stay off-screen) */
const PERSON_DROP = 190;
const personShift = (frame: number) =>
  interpolate(frame, [f(E.trees) - 6, f(E.trees) + 10], [0, PERSON_DROP], { ...clamp, easing: Easing.inOut(Easing.cubic) });

/** head top / centre / width in output pixels, after the person scale */
const headAt = (frame: number) => {
  const [top, cx, hw] = D.head[Math.max(0, Math.min(D.head.length - 1, frame))] as number[];
  return { top: top + personShift(frame), cx, hw, s: 1 };
};

/* ------------------------------------------------------- pink world */
const PinkBackground: React.FC = () => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse 90% 70% at 50% 35%, ${PINK_A} 0%, ${PINK_B} 100%)` }} />
);

/* ---------------------------------------------------------- cascade */
const POSTS = new Array(10).fill(0).map((_, i) => staticFile(`posts/p${String(i).padStart(2, "0")}.jpg`));
const Cascade: React.FC = () => {
  const frame = useCurrentFrame(); // local, 0 = cascade start
  const cols = [
    { x: 30, speed: 9.5, delay: 0, rot: -4 },
    { x: 300, speed: 8.2, delay: 6, rot: 3 },
    { x: 560, speed: 10.4, delay: 3, rot: -2 },
    { x: 830, speed: 8.8, delay: 9, rot: 4 },
  ];
  const TW = 230;
  const TH = 306;
  const GAP = 34;
  return (
    <AbsoluteFill>
      {cols.map((c, ci) => {
        const fr = frame - c.delay;
        if (fr < 0) return null;
        // the first tiles fall in with a little acceleration, then the column flows steadily
        const dist = fr * c.speed + 0.5 * 0.9 * Math.min(fr, 18) ** 2;
        const tiles = [];
        for (let k = 0; k < 9; k++) {
          const y = dist - TH - k * (TH + GAP) - 40;
          if (y < -TH - 20 || y > 1940) continue;
          const post = POSTS[(ci * 3 + k) % POSTS.length];
          tiles.push(
            <Img
              key={k}
              src={post}
              style={{
                position: "absolute",
                left: c.x,
                top: y,
                width: TW,
                height: TH,
                objectFit: "cover",
                borderRadius: 22,
                border: "6px solid #fff",
                boxShadow: "0 18px 40px rgba(120,60,70,0.35)",
                transform: `rotate(${c.rot * (k % 2 ? -1 : 1)}deg)`,
              }}
            />,
          );
        }
        return <React.Fragment key={ci}>{tiles}</React.Fragment>;
      })}
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------ trees */
const Tree: React.FC<{ h: number; grow: number; canopy: number; sway: number; blossom?: boolean }> = ({ h, grow, canopy, sway, blossom }) => {
  const w = h * 0.9;
  return (
    <svg width={w} height={h} viewBox="0 0 100 110" style={{ overflow: "visible", transformOrigin: "50% 100%", transform: `rotate(${sway}deg)` }}>
      <g style={{ transformOrigin: "50px 110px", transform: `scaleY(${grow})` }}>
        <path d="M46 110 C47 85, 44 70, 48 52 L52 52 C55 70, 53 85, 54 110 Z" fill="#7A4E2D" />
        <path d="M49 72 C40 64, 36 60, 32 54" stroke="#7A4E2D" strokeWidth={3.2} fill="none" strokeLinecap="round" />
        <path d="M51 66 C60 58, 64 55, 69 50" stroke="#7A4E2D" strokeWidth={3} fill="none" strokeLinecap="round" />
      </g>
      <g style={{ transformOrigin: "50px 52px", transform: `scale(${canopy})` }}>
        <circle cx={50} cy={34} r={27} fill="#4E8F45" />
        <circle cx={30} cy={48} r={19} fill="#5FA052" />
        <circle cx={70} cy={46} r={20} fill="#5FA052" />
        <circle cx={50} cy={22} r={19} fill="#74B85F" />
        <circle cx={38} cy={30} r={13} fill="#86C76E" />
        <circle cx={62} cy={32} r={12} fill="#7DBE66" />
        <circle cx={43} cy={20} r={6} fill="#A8DB8E" opacity={0.8} />
        {blossom
          ? [[30, 40], [58, 18], [70, 40], [44, 46], [52, 30], [24, 52], [76, 52]].map(([x, y], i) => (
              <circle key={i} cx={x} cy={y} r={3.4} fill="#F7A6B9" stroke="#fff" strokeWidth={0.8} />
            ))
          : null}
      </g>
    </svg>
  );
};

const Trees: React.FC = () => {
  const frame = useCurrentFrame(); // local
  const { fps } = useVideoConfig();
  const abs = frame + f(E.trees);
  const { top, cx, hw, s } = headAt(abs);
  const trees = [
    { dx: -0.3, h: 420, delay: 2, blossom: true },
    { dx: 0.02, h: 540, delay: 0, blossom: false },
    { dx: 0.32, h: 390, delay: 5, blossom: true },
  ];
  return (
    <AbsoluteFill>
      {trees.map((t, i) => {
        const lf = frame - t.delay;
        const grow = interpolate(lf, [0, 11], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
        const canopy = spring({ frame: lf - 7, fps, config: { damping: 9, stiffness: 140, mass: 0.7 } });
        const h = t.h * s;
        const sway = Math.sin((abs + i * 20) / 22) * 2.2;
        return (
          <div key={i} style={{ position: "absolute", left: cx + t.dx * hw - (h * 0.9) / 2, top: top + 150 * s - h }}>
            <Tree h={h} grow={grow} canopy={canopy} sway={sway} blossom={t.blossom} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------- sparkles */
const Sparkles: React.FC<{ seed: number }> = ({ seed }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const abs = frame + f(E.pink);
  const { top, cx } = headAt(abs);
  const n = 26;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {new Array(n).fill(0).map((_, i) => {
        const a = ((i * 137.5 + seed) % 360) * (Math.PI / 180);
        const r = interpolate(frame, [0, durationInFrames], [80, 520 + (i % 5) * 60], { ...clamp, easing: Easing.out(Easing.cubic) });
        const o = interpolate(frame, [0, 4, durationInFrames - 6, durationInFrames], [0, 1, 1, 0], clamp);
        const size = 18 + (i % 4) * 10;
        return (
          <div key={i} style={{ position: "absolute", left: cx + Math.cos(a) * r - size / 2, top: top + 380 + Math.sin(a) * r * 1.2 - size / 2, fontSize: size, opacity: o, transform: `rotate(${frame * 8 + i * 20}deg)`, color: i % 3 ? "#fff" : ACCENT, textShadow: "0 0 12px rgba(255,255,255,0.9)" }}>
            ✦
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/** everything that exists only in the edited "AI" world, revealed by a circle growing from her head */
const MagicWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const start = f(E.pink);
  const r = interpolate(frame, [start, start + 16], [0, 2300], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  if (frame < D.personFrom) return null;
  const { top, cx } = headAt(Math.max(frame, start));
  const ty = personShift(frame);
  return (
    <AbsoluteFill style={{ clipPath: `circle(${r}px at ${cx}px ${top + 400}px)` }}>
      <PinkBackground />
      <Sequence name="Cascadă postări" from={f(E.cascade)}>
        <Cascade />
      </Sequence>
      <Sequence name="Copaci" from={f(E.trees)}>
        <Trees />
      </Sequence>
      <AbsoluteFill style={{ transform: `translateY(${ty}px)` }}>
        <PersonCuts />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------- overlays */
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const p = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });
  const out = interpolate(frame, [durationInFrames - 6, durationInFrames], [1, 0], clamp);
  const mic = spring({ frame: frame - f(E.mic), fps, config: { damping: 11, stiffness: 220 } });
  const cam = spring({ frame: frame - f(E.cam), fps, config: { damping: 11, stiffness: 220 } });
  const icon = (e: string, s: number) => (
    <div style={{ position: "relative", width: 150, height: 150, borderRadius: 75, background: "rgba(255,255,255,0.92)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 84, transform: `scale(${s})`, boxShadow: shadow }}>
      {e}
      <div style={{ position: "absolute", width: 150, height: 12, borderRadius: 6, background: "#E5484D", transform: `rotate(-40deg) scaleX(${Math.min(1, s)})` }} />
    </div>
  );
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: "absolute", top: 120, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
        <div style={{ transform: `scale(${p})`, display: "flex", alignItems: "center", gap: 18, background: PAPER, borderRadius: 999, padding: "14px 36px 14px 18px", boxShadow: shadow, fontFamily: SANS, fontWeight: 900, fontSize: 50, color: INK }}>
          <span style={{ width: 74, height: 74, borderRadius: 37, background: "#FBEDE6", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <ClaudeMark size={50} rotate={frame} />
          </span>
          1 poză + <span style={{ fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, fontSize: 64, color: ACCENT }}>Claude</span>
        </div>
      </div>
      <div style={{ position: "absolute", top: 1170, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 60 }}>
        {icon("🎙️", mic)}
        {icon("📷", cam)}
      </div>
    </AbsoluteFill>
  );
};

/** her prompt, typed word-by-word as she says it, like a chat message */
const PromptBubble: React.FC<{ n: number; start: number; send: number; words: { text: string; start: number }[] }> = ({ n, start, send, words }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps + start;
  const enter = spring({ frame, fps, config: { damping: 15, stiffness: 190 } });
  const sent = frame >= f(send) - f(start);
  const fly = interpolate(frame, [durationInFrames - 7, durationInFrames], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
  const shown = words.filter((w) => t >= w.start);
  const caret = Math.floor(frame / 8) % 2 === 0;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, right: 70, top: 1330, display: "flex", flexDirection: "column", alignItems: "flex-end", transform: `translateY(${(1 - enter) * 120 - fly * 260}px) scale(${1 - fly * 0.25})`, opacity: Math.min(enter * 1.5, 1 - fly) }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12, marginRight: 8, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: "#fff", textShadow: "0 2px 10px rgba(0,0,0,0.6)" }}>
          <ClaudeMark size={30} color="#fff" /> Promptul #{n} pentru Claude
        </div>
        <div style={{ background: "#fff", borderRadius: "40px 40px 10px 40px", padding: "28px 34px", maxWidth: 900, boxShadow: shadow, display: "flex", alignItems: "flex-end", gap: 20 }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 52, lineHeight: 1.22, color: INK }}>
            {shown.map((w) => w.text).join(" ")}
            {!sent ? <span style={{ display: "inline-block", width: 5, height: 50, marginLeft: 6, verticalAlign: "-0.1em", background: ACCENT, opacity: caret ? 1 : 0 }} /> : null}
          </span>
          <div style={{ width: 70, height: 70, borderRadius: 35, background: sent ? ACCENT : "#E8E2D8", color: "#fff", fontSize: 40, fontWeight: 900, fontFamily: SANS, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, transform: `scale(${sent ? 1.12 : 1})` }}>↑</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Gata: React.FC<{ emoji: string }> = ({ emoji }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 8, stiffness: 200, mass: 0.6 } });
  const out = interpolate(frame, [durationInFrames - 6, durationInFrames], [1, 0], clamp);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 1370, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: out }}>
        <div style={{ transform: `scale(${s}) rotate(-4deg)`, fontFamily: SERIF, fontStyle: "italic", fontSize: 190, color: "#fff", lineHeight: 1, textShadow: `0 6px 0 ${ACCENT}, 0 12px 40px rgba(0,0,0,0.45)` }}>
          Și gata! <span style={{ fontStyle: "normal", fontSize: 140 }}>{emoji}</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Academy: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const st = E.academy.start;
  const card = spring({ frame, fps, config: { damping: 14, stiffness: 170 } });
  const wake = spring({ frame: frame - (f(E.academy.wake) - f(st)), fps, config: { damping: 11, stiffness: 170 } });
  const ro = spring({ frame: frame - (f(E.academy.ro) - f(st)), fps, config: { damping: 9, stiffness: 190, mass: 0.7 } });
  const band = interpolate(frame, [f(E.academy.ro) - f(st), f(E.academy.ro) - f(st) + 12], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const end = interpolate(frame, [durationInFrames - 5, durationInFrames], [1, 0.9], clamp);
  return (
    <AbsoluteFill style={{ opacity: end }}>
      <div style={{ position: "absolute", left: 70, right: 70, top: 1310, display: "flex", justifyContent: "center", transform: `translateY(${(1 - card) * 200}px)`, opacity: Math.min(1, card * 1.5) }}>
        <div style={{ background: PAPER, borderRadius: 44, padding: "34px 44px 30px", boxShadow: shadow, display: "flex", flexDirection: "column", alignItems: "center", gap: 6, minWidth: 820 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 18, fontFamily: SANS, fontWeight: 900, fontSize: 62, color: INK, letterSpacing: -1.5 }}>
            🎓 Academia Digitală
          </div>
          <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 96, color: ACCENT, lineHeight: 1.05, opacity: wake, transform: `scale(${0.7 + 0.3 * wake})` }}>
            Deșteaptă-te, <span style={{ transform: `scale(${ro})`, display: "inline-block" }}>Române!</span>
          </div>
          <div style={{ display: "flex", width: 560 * band, height: 14, borderRadius: 7, overflow: "hidden", marginTop: 8 }}>
            <div style={{ flex: 1, background: "#002B7F" }} />
            <div style={{ flex: 1, background: "#FCD116" }} />
            <div style={{ flex: 1, background: "#CE1126" }} />
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------- captions */
type CW = { text: string; start: number; end: number; key: boolean };
const OUTLINE = "0 0 2px #000, 0 4px 0 rgba(0,0,0,0.85), 0 6px 22px rgba(0,0,0,0.55)";
const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const page = D.captions.find((c) => t >= c.start && t < c.end);
  if (!page) return null;
  const words = page.words as CW[];
  const last = words.reduce((acc, x, j) => (t >= x.start ? j : acc), -1);
  const pin = spring({ frame: frame - Math.round(page.start * FPS), fps: FPS, config: { damping: 15, stiffness: 260 }, durationInFrames: 7 });
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top: 1540, height: 220, display: "flex", flexWrap: "wrap", alignContent: "center", justifyContent: "center", columnGap: 18, opacity: pin, transform: `translateY(${(1 - pin) * 24}px)` }}>
      {words.map((w, i) => {
        const active = i === last && t < w.end + 0.25;
        return (
          <span key={i} style={{ fontFamily: w.key ? SERIF : SANS, fontStyle: w.key ? "italic" : "normal", fontWeight: w.key ? 400 : 900, fontSize: w.key ? 106 : 84, lineHeight: 1.12, letterSpacing: w.key ? 0 : -1.2, color: active ? ACCENT : "#fff", textShadow: OUTLINE, padding: w.key ? "0 8px 0 2px" : 0, transform: `scale(${active ? 1.06 : 1})`, display: "inline-block" }}>
            {w.text}
          </span>
        );
      })}
    </div>
  );
};

/* ------------------------------------------------------------- sound */
const GAIN: Record<string, number> = { whoosh: 0.11, pop: 0.076, typing: 0.19, send: 0.122, sparkle: 0.153, grow: 0.15, cascade: 0.212, sting: 0.15, ding: 0.075 };
const Sound: React.FC = () => {
  const total = D.durationInFrames;
  const dist = (t: number) => {
    let d = Infinity;
    for (const [s, e] of D.speech as [number, number][]) {
      if (t >= s && t <= e) return 0;
      d = Math.min(d, Math.abs(t - s), Math.abs(t - e));
    }
    return d;
  };
  return (
    <>
      <Audio
        name="Lo-fi music"
        src={staticFile("sfx/lofi.wav")}
        loop
        loopVolumeCurveBehavior="extend"
        volume={(fr) =>
          interpolate(dist(fr / FPS), [0.05, 0.35], [0.083, 0.21], clamp) * interpolate(fr, [0, 12, total - 40, total], [0, 1, 1, 0], clamp)
        }
      />
      {(D.sfx as { t: number; type: string; dur: number }[]).map((e, i) => {
        const looped = e.dur > 0;
        const frames = looped ? Math.max(1, Math.round(e.dur * FPS)) : 60;
        return (
          <Sequence key={i} name={`SFX ${e.type}`} from={Math.round(e.t * FPS)} durationInFrames={frames}>
            <Audio
              src={staticFile(`sfx/${e.type}.wav`)}
              loop={looped}
              volume={(fr) => (looped ? GAIN[e.type] * interpolate(fr, [0, 3, frames - 4, frames], [0, 1, 1, 0], clamp) : GAIN[e.type])}
            />
          </Sequence>
        );
      })}
    </>
  );
};

/* ============================================================ main */
export const Academia: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ filter: "contrast(1.05) saturate(1.08)" }}>
        <BaseCuts />
        <MagicWorld />
      </AbsoluteFill>
      <Sequence name="Sclipici" from={f(E.pink)} durationInFrames={24}>
        <Sparkles seed={11} />
      </Sequence>
      <Sequence name="Hook" from={0} durationInFrames={f(E.hook.end)}>
        <Hook />
      </Sequence>
      {E.prompts.map((p) => (
        <Sequence key={p.n} name={`Prompt ${p.n}`} from={f(p.start)} durationInFrames={f(p.end) - f(p.start)}>
          <PromptBubble n={p.n} start={p.start} send={p.send} words={p.words} />
        </Sequence>
      ))}
      {E.gata.map((g, i) => (
        <Sequence key={i} name={`Și gata ${i + 1}`} from={f(g.start)} durationInFrames={f(g.end) - f(g.start)}>
          <Gata emoji={["🌸", "🌳", "🖼️"][i]} />
        </Sequence>
      ))}
      <Sequence name="Academia Digitală" from={f(E.academy.start)}>
        <Academy />
      </Sequence>
      <Captions />
      <div style={{ position: "absolute", left: 0, top: 0, height: 10, width: `${(frame / (D.durationInFrames - 1)) * 100}%`, background: ACCENT }} />
      <Sound />
    </AbsoluteFill>
  );
};
