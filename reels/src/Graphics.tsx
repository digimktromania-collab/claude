import React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ClaudeMark } from "./Logos";
import { ACCENT, cardShadow, f, INK, PAPER, SANS, SERIF, TL } from "./lib";

const S = TL.scenes;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const GREY = "#8A8478";
const LINE = "#E6E0D4";

/* ------------------------------------------------------------ helpers */
const At: React.FC<{ start: number; end: number; name: string; children: React.ReactNode }> = ({ start, end, name, children }) => (
  <Sequence name={name} from={f(start)} durationInFrames={Math.max(1, f(end) - f(start))} premountFor={30}>
    {children}
  </Sequence>
);

/** local frame of an absolute output time, relative to a scene start */
const rel = (abs: number, start: number) => f(abs) - f(start);

const pop = (frame: number, at: number, fps: number) =>
  spring({ frame: frame - at, fps, config: { damping: 12, stiffness: 210, mass: 0.6 } });

const useScene = (exit = 6) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 16, stiffness: 170, mass: 0.8 } });
  const out = interpolate(frame, [durationInFrames - exit, durationInFrames], [1, 0], clamp);
  return { frame, fps, enter, out, v: Math.min(enter, out) };
};

const Italic: React.FC<{ children: React.ReactNode; size?: number; color?: string }> = ({ children, size, color }) => (
  <span style={{ fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, fontSize: size, color }}>{children}</span>
);

const Box: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div style={{ background: "#fff", borderRadius: 34, boxShadow: "0 18px 50px rgba(31,30,29,0.14), 0 4px 12px rgba(31,30,29,0.08)", border: `2px solid ${LINE}`, color: INK, fontFamily: SANS, ...style }}>
    {children}
  </div>
);

/** content area inside the panel: below the chapter pill, above the captions */
const Content: React.FC<{ v: number; children: React.ReactNode; top?: number }> = ({ v, children, top = 250 }) => (
  <div style={{ position: "absolute", left: 60, right: 60, top, height: 720 - top, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: Math.min(1, v * 1.5), transform: `translateY(${(1 - v) * 60}px)` }}>
    {children}
  </div>
);

const Typewriter: React.FC<{ text: string; start: number; end: number; size: number }> = ({ text, start, end, size }) => {
  const frame = useCurrentFrame();
  const n = Math.round(interpolate(frame, [start, Math.max(start + 1, end)], [0, text.length], clamp));
  const caret = n < text.length || Math.floor(frame / 9) % 2 === 0;
  return (
    <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: size, lineHeight: 1.3, color: INK }}>
      {text.slice(0, n)}
      <span style={{ display: "inline-block", width: 4, height: size, marginLeft: 3, verticalAlign: "-0.12em", background: ACCENT, opacity: caret ? 1 : 0 }} />
    </span>
  );
};

/* ------------------------------------------------- chapter pill (panel) */
const Chapter: React.FC<{ n: string; label: string }> = ({ n, label }) => {
  const { frame, fps, out } = useScene(4);
  const s = pop(frame, 0, fps);
  return (
    <div style={{ position: "absolute", top: 140, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: out }}>
      <div style={{ transform: `scale(${s})`, display: "flex", alignItems: "center", gap: 16, background: INK, color: "#fff", borderRadius: 999, padding: "12px 34px 12px 14px", fontFamily: SANS, fontWeight: 900, fontSize: 38, letterSpacing: 2 }}>
        <span style={{ width: 54, height: 54, borderRadius: 27, background: ACCENT, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 32, letterSpacing: 0 }}>{n}</span>
        {label}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------ ① IDEAS */
const Ideas: React.FC = () => {
  const { frame, fps, v } = useScene();
  const twoAt = rel(S.ideas.two, S.ideas.start);
  const cards = [
    { n: "1", e: "🖼️", t: "Redimensionează", s: "poze pentru social media" },
    { n: "2", e: "⏰", t: "Reminder", s: "să postezi zilnic" },
  ];
  return (
    <Content v={v}>
      <div style={{ display: "flex", gap: 34 }}>
        {cards.map((c, i) => {
          const s = pop(frame, twoAt + i * 5, fps);
          return (
            <Box key={c.n} style={{ width: 410, height: 380, padding: 30, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 10, transform: `scale(${s}) rotate(${(1 - s) * (i ? 8 : -8)}deg)`, opacity: Math.min(1, s * 2) }}>
              <div style={{ width: 58, height: 58, borderRadius: 29, background: ACCENT, color: "#fff", fontWeight: 900, fontSize: 34, display: "flex", alignItems: "center", justifyContent: "center" }}>{c.n}</div>
              <div style={{ fontSize: 110, lineHeight: 1.1 }}>{c.e}</div>
              <div style={{ fontWeight: 900, fontSize: 44, letterSpacing: -1 }}>{c.t}</div>
              <div style={{ fontWeight: 600, fontSize: 30, color: GREY, textAlign: "center" }}>{c.s}</div>
            </Box>
          );
        })}
      </div>
    </Content>
  );
};

/* --------------------------------------------------- idea cards (#1/#2) */
const IdeaCard: React.FC<{ n: string; emoji: string; title: string; prompt: string; typeStart: number; typeEnd: number; footer: React.ReactNode }> = ({ n, emoji, title, prompt, typeStart, typeEnd, footer }) => {
  const { v } = useScene();
  return (
    <Content v={v}>
      <Box style={{ width: "100%", padding: "30px 38px 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 20 }}>
          <div style={{ width: 84, height: 84, borderRadius: 24, background: "#FBEDE6", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 52 }}>{emoji}</div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <span style={{ fontWeight: 800, fontSize: 28, color: ACCENT, letterSpacing: 2 }}>IDEEA #{n}</span>
            <span style={{ fontWeight: 900, fontSize: 46, letterSpacing: -1 }}>{title}</span>
          </div>
        </div>
        <div style={{ background: "#F7F4EE", borderRadius: 22, padding: "20px 26px", minHeight: 170 }}>
          <div style={{ fontWeight: 800, fontSize: 24, color: GREY, marginBottom: 6, letterSpacing: 1 }}>PROMPTUL TĂU ↓</div>
          <Typewriter text={prompt} start={typeStart} end={typeEnd} size={40} />
        </div>
        {footer}
      </Box>
    </Content>
  );
};

const Chip: React.FC<{ s: number; bg: string; color?: string; children: React.ReactNode }> = ({ s, bg, color = "#fff", children }) => (
  <div style={{ transform: `scale(${s})`, opacity: Math.min(1, s * 2), background: bg, color, borderRadius: 999, padding: "12px 26px", fontFamily: SANS, fontWeight: 900, fontSize: 32, whiteSpace: "nowrap" }}>{children}</div>
);

const App1: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const st = S.app1.start;
  return (
    <IdeaCard
      n="1"
      emoji="🖼️"
      title="Resize poze pe desktop"
      prompt="Creează o aplicație pe desktop care redimensionează pozele pentru Facebook, TikTok și Instagram."
      typeStart={rel(S.app1.prompt, st)}
      typeEnd={rel(S.app1.ig, st)}
      footer={
        <div style={{ display: "flex", gap: 14, marginTop: 22, justifyContent: "center" }}>
          <Chip s={pop(frame, rel(S.app1.fb, st), fps)} bg="#1877F2">Facebook</Chip>
          <Chip s={pop(frame, rel(S.app1.tt, st), fps)} bg="#111">TikTok</Chip>
          <Chip s={pop(frame, rel(S.app1.ig, st), fps)} bg="linear-gradient(45deg,#F58529,#DD2A7B,#8134AF)">Instagram</Chip>
        </div>
      }
    />
  );
};

const App2: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const st = S.app2.start;
  const c = pop(frame, rel(S.app2.clock, st), fps);
  return (
    <IdeaCard
      n="2"
      emoji="⏰"
      title="Reminder de postare"
      prompt="Creează o aplicație care să-mi amintească în fiecare zi să postez pe TikTok la ora 18."
      typeStart={rel(S.app2.prompt, st)}
      typeEnd={rel(S.app2.clock, st)}
      footer={
        <div style={{ display: "flex", gap: 14, marginTop: 22, justifyContent: "center" }}>
          <Chip s={c} bg={ACCENT}>🕕 18:00</Chip>
          <Chip s={pop(frame, rel(S.app2.clock, st) + 5, fps)} bg="#111">în fiecare zi</Chip>
        </div>
      }
    />
  );
};

/* -------------------------------------------- notification on desktop */
const Notif: React.FC = () => {
  const { frame, fps, v } = useScene();
  const at = rel(S.notif.banner, S.notif.start);
  const b = spring({ frame: frame - at, fps, config: { damping: 14, stiffness: 150 } });
  return (
    <Content v={v}>
      <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 52, color: INK, marginBottom: 22, letterSpacing: -1 }}>
        Îți trimite <Italic size={66} color={ACCENT}>notificări</Italic> 🔔
      </div>
      <div style={{ position: "relative", width: 900, height: 330, borderRadius: 30, overflow: "hidden", background: "linear-gradient(135deg,#F2B8A0 0%,#D97757 45%,#7A4B9A 100%)", boxShadow: cardShadow }}>
        <div style={{ height: 44, background: "rgba(255,255,255,0.35)", display: "flex", alignItems: "center", padding: "0 20px", gap: 22, fontFamily: SANS, fontWeight: 700, fontSize: 22, color: INK }}>
          <span></span><span>Finder</span><span style={{ marginLeft: "auto" }}>18:00</span>
        </div>
        <div style={{ position: "absolute", right: 22, top: 66, width: 600, transform: `translateX(${(1 - b) * 680}px)`, background: "rgba(255,255,255,0.93)", borderRadius: 24, padding: "20px 24px", display: "flex", gap: 18, boxShadow: "0 12px 30px rgba(0,0,0,0.25)" }}>
          <div style={{ width: 76, height: 76, borderRadius: 18, background: ACCENT, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
            <ClaudeMark size={50} color="#fff" />
          </div>
          <div style={{ fontFamily: SANS, color: INK }}>
            <div style={{ display: "flex", gap: 10, alignItems: "baseline" }}>
              <span style={{ fontWeight: 900, fontSize: 30 }}>Reminder TikTok</span>
              <span style={{ fontWeight: 600, fontSize: 22, color: GREY }}>acum</span>
            </div>
            <div style={{ fontWeight: 600, fontSize: 28, lineHeight: 1.25 }}>E ora 18:00 — postează pe TikTok! 🎬</div>
          </div>
        </div>
      </div>
    </Content>
  );
};

/* ---------------------------------------------------------- share */
const Share: React.FC = () => {
  const { frame, fps, v } = useScene();
  const st = S.share.start;
  const btn = pop(frame, rel(S.share.btn, st), fps);
  const ppl = ["#D97757", "#2E7DD7", "#1F9D55", "#8E5BD0"];
  const names = ["A", "M", "R", "+3"];
  const team = pop(frame, rel(S.share.team, st), fps);
  return (
    <Content v={v}>
      <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 52, color: INK, marginBottom: 30, letterSpacing: -1 }}>
        O poți <Italic size={66} color={ACCENT}>da mai departe</Italic>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 30 }}>
        <div style={{ transform: `scale(${btn})`, background: INK, color: "#fff", fontFamily: SANS, fontWeight: 900, fontSize: 46, borderRadius: 26, padding: "26px 40px", boxShadow: cardShadow }}>🔗 Share</div>
        <div style={{ fontSize: 60, color: INK, opacity: btn }}>→</div>
        <div style={{ display: "flex" }}>
          {ppl.map((c, i) => {
            const s = pop(frame, rel(S.share.people, st) + i * 3, fps);
            return (
              <div key={i} style={{ width: 120, height: 120, borderRadius: 60, background: c, border: "6px solid #F4F0E8", marginLeft: i ? -26 : 0, transform: `scale(${s})`, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontFamily: SANS, fontWeight: 900, fontSize: 44 }}>
                {names[i]}
              </div>
            );
          })}
        </div>
      </div>
      <div style={{ marginTop: 26, transform: `scale(${team})`, fontFamily: SANS, fontWeight: 800, fontSize: 40, color: GREY }}>prieteni · colegi · echipa ta</div>
    </Content>
  );
};

/* --------------------------------------------------- ② HOW: 3 steps */
const Cursor: React.FC<{ x: number; y: number; down: boolean }> = ({ x, y, down }) => (
  <svg width={56} height={56} viewBox="0 0 24 24" style={{ position: "absolute", left: x, top: y, transform: `scale(${down ? 0.82 : 1})`, filter: "drop-shadow(0 4px 6px rgba(0,0,0,.35))" }}>
    <path d="M4 2 L4 20 L9 15 L12.5 22 L15.5 20.5 L12 13.5 L19 13.5 Z" fill="#111" stroke="#fff" strokeWidth={1.4} strokeLinejoin="round" />
  </svg>
);

const Stepper: React.FC<{ step: number }> = ({ step }) => {
  const steps = ["Scrii promptul", "Claude lucrează", "Install App"];
  return (
    <div style={{ position: "absolute", top: 225, left: 60, right: 60, display: "flex", gap: 12 }}>
      {steps.map((s, i) => {
        const active = i === step;
        const done = i < step;
        return (
          <div key={s} style={{ flex: 1, display: "flex", alignItems: "center", gap: 10, background: active ? ACCENT : done ? "#fff" : "rgba(255,255,255,0.55)", color: active ? "#fff" : INK, border: `2px solid ${active ? ACCENT : LINE}`, borderRadius: 18, padding: "12px 14px", fontFamily: SANS, fontWeight: 900, fontSize: 27, opacity: active || done ? 1 : 0.6 }}>
            <span style={{ width: 40, height: 40, borderRadius: 20, background: active ? "#fff" : done ? "#1F9D55" : LINE, color: active ? ACCENT : "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24, flexShrink: 0 }}>{done ? "✓" : i + 1}</span>
            {s}
          </div>
        );
      })}
    </div>
  );
};

const StepPrompt: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const sendAt = rel(S.how.send, S.how.start);
  const sent = pop(frame, sendAt, fps);
  return (
    <Box style={{ width: "100%", padding: "28px 30px", display: "flex", flexDirection: "column", gap: 18 }}>
      <div style={{ fontWeight: 800, fontSize: 28, color: GREY }}>Scrie în Claude ce aplicație vrei:</div>
      <div style={{ display: "flex", alignItems: "flex-end", gap: 18, background: "#F7F4EE", borderRadius: 24, padding: "20px 20px 20px 26px", border: `3px solid ${sent > 0.5 ? ACCENT : LINE}` }}>
        <div style={{ flex: 1, minHeight: 110 }}>
          <Typewriter text="Creează o aplicație care să-mi amintească să postez pe TikTok la ora 18." start={4} end={sendAt - 2} size={38} />
        </div>
        <div style={{ width: 78, height: 78, borderRadius: 39, background: ACCENT, color: "#fff", fontSize: 44, fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${1 + 0.25 * Math.sin(Math.min(1, sent) * Math.PI)})`, flexShrink: 0 }}>↑</div>
      </div>
    </Box>
  );
};

const StepArtifact: React.FC<{ frame: number }> = ({ frame }) => {
  const lines = [0.9, 0.6, 0.75, 0.5];
  return (
    <Box style={{ width: "100%", overflow: "hidden" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "20px 28px", borderBottom: `2px solid ${LINE}` }}>
        <ClaudeMark size={44} rotate={frame * 4} />
        <span style={{ fontWeight: 900, fontSize: 34 }}>Artefact</span>
        <span style={{ fontWeight: 700, fontSize: 28, color: GREY, marginLeft: "auto" }}>Claude lucrează…</span>
      </div>
      <div style={{ padding: "26px 28px", display: "flex", gap: 24 }}>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 18 }}>
          {lines.map((w, i) => (
            <div key={i} style={{ height: 24, borderRadius: 12, width: `${w * 100 * Math.min(1, Math.max(0, (frame - i * 6) / 14))}%`, background: i === 0 ? "#F0C9B8" : LINE }} />
          ))}
        </div>
        <div style={{ width: 230, height: 150, borderRadius: 18, background: "#F7F4EE", display: "flex", alignItems: "center", justifyContent: "center", gap: 10 }}>
          {[0, 1, 2].map((i) => (
            <div key={i} style={{ width: 52, height: [70, 100, 60][i], borderRadius: 10, background: i === 1 ? ACCENT : "#DCD5C7", transform: `scaleY(${Math.min(1, Math.max(0, (frame - 10 - i * 5) / 10))})` }} />
          ))}
        </div>
      </div>
    </Box>
  );
};

const StepInstall: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const st = S.how.start;
  const dotsAt = rel(S.how.dots, st) - rel(S.how.s3, st);
  const instAt = rel(S.how.install, st) - rel(S.how.s3, st);
  const menu = spring({ frame: frame - dotsAt - 3, fps, config: { damping: 16, stiffness: 220 } });
  const ring = interpolate(frame, [dotsAt - 4, dotsAt + 6], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const marker = interpolate(frame, [instAt, instAt + 9], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  // cursor path: start -> ⋯ button -> "Install as app"
  const DOTS = { x: 840, y: 52 };
  const INSTALL = { x: 520, y: 330 };
  const toDots = interpolate(frame, [0, dotsAt], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const toInst = interpolate(frame, [instAt - 12, instAt], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const cx = interpolate(toDots, [0, 1], [460, DOTS.x]) + (INSTALL.x - DOTS.x) * toInst;
  const cy = interpolate(toDots, [0, 1], [300, DOTS.y]) + (INSTALL.y - DOTS.y) * toInst;
  const down = (frame >= dotsAt && frame < dotsAt + 4) || (frame >= instAt && frame < instAt + 4);
  const rows = [
    { i: "⧉", t: "Copy" },
    { i: "⤓", t: "Download" },
    { i: "↗", t: "Publish" },
    { i: "⊕", t: "Install as app" },
  ];
  return (
    <div style={{ position: "relative", width: 960, height: 420 }}>
      <Box style={{ position: "absolute", left: 0, top: 0, width: 960, height: 104, padding: "0 30px", display: "flex", alignItems: "center", borderRadius: 26 }}>
        <span style={{ fontWeight: 900, fontSize: 38 }}>✳︎ Reminder TikTok</span>
        <div style={{ marginLeft: "auto", position: "relative", width: 86, height: 62, borderRadius: 16, background: "#F0EDE5", display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
          {[0, 1, 2].map((i) => <i key={i} style={{ width: 11, height: 11, borderRadius: 6, background: INK, display: "block" }} />)}
          <svg width={140} height={110} viewBox="0 0 140 110" style={{ position: "absolute", left: -27, top: -24, overflow: "visible" }}>
            <ellipse cx={70} cy={55} rx={64} ry={46} fill="none" stroke={ACCENT} strokeWidth={6} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ring} />
          </svg>
        </div>
      </Box>
      <Box style={{ position: "absolute", right: 0, top: 120, width: 560, padding: "10px 0", transformOrigin: "top right", transform: `scale(${menu})`, opacity: menu }}>
        {rows.map((r, i) => {
          const last = i === rows.length - 1;
          return (
            <div key={r.t} style={{ position: "relative", height: 70, display: "flex", alignItems: "center", gap: 20, padding: "0 30px", fontSize: 34, fontWeight: last ? 900 : 600, background: last && marker > 0 ? "#FBEDE6" : "transparent", color: INK }}>
              <span style={{ width: 36, textAlign: "center" }}>{r.i}</span>
              {r.t}
              {last ? (
                <svg width={300} height={20} viewBox="0 0 300 20" style={{ position: "absolute", left: 82, top: 56, overflow: "visible" }}>
                  <path d="M 4 10 C 80 4, 200 16, 296 8" fill="none" stroke={ACCENT} strokeWidth={10} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - marker} />
                </svg>
              ) : null}
            </div>
          );
        })}
      </Box>
      <Cursor x={cx} y={cy} down={down} />
    </div>
  );
};

const How: React.FC = () => {
  const { frame, fps, v } = useScene();
  const st = S.how.start;
  const s2 = rel(S.how.s2, st);
  const s3 = rel(S.how.s3, st);
  const step = frame < s2 ? 0 : frame < s3 ? 1 : 2;
  const local = step === 0 ? frame : step === 1 ? frame - s2 : frame - s3;
  const swap = spring({ frame: local, fps, config: { damping: 16, stiffness: 190 } });
  return (
    <>
      <div style={{ opacity: v }}>
        <Stepper step={step} />
      </div>
      <div style={{ position: "absolute", left: 60, right: 60, top: 320, height: 400, display: "flex", alignItems: "center", justifyContent: "center", opacity: Math.min(v, swap), transform: `translateX(${(1 - swap) * 120}px)` }}>
        {step === 0 ? <StepPrompt frame={frame} fps={fps} /> : step === 1 ? <StepArtifact frame={local} /> : <StepInstall frame={local} fps={fps} />}
      </div>
    </>
  );
};

const Recap: React.FC = () => {
  const { frame, fps, v } = useScene();
  const a = pop(frame, 0, fps);
  const b = pop(frame, rel(S.recap.second, S.recap.start), fps);
  return (
    <Content v={v}>
      <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 50, color: INK, marginBottom: 30 }}>
        Pe scurt <Italic size={64} color={ACCENT}>doar 2 pași</Italic>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
        <Box style={{ transform: `scale(${a})`, padding: "28px 34px", fontWeight: 900, fontSize: 46, whiteSpace: "nowrap" }}>💬 Creează app</Box>
        <span style={{ fontSize: 64, fontWeight: 900, color: INK, opacity: b }}>→</span>
        <div style={{ transform: `scale(${b})`, background: ACCENT, color: "#fff", borderRadius: 34, padding: "28px 34px", fontFamily: SANS, fontWeight: 900, fontSize: 46, whiteSpace: "nowrap", boxShadow: cardShadow }}>⊕ Install app</div>
      </div>
    </Content>
  );
};

/* =========================== full-screen graphics (above head / on chest) */
const Hook: React.FC = () => {
  const { frame, fps, v } = useScene(6);
  const tile = pop(frame, 0, fps);
  const band = spring({ frame: frame - 3, fps, config: { damping: 17, stiffness: 150 } });
  const freeAt = rel(S.hook.free, S.hook.start);
  const free = pop(frame, freeAt, fps);
  const nou = pop(frame, 10, fps);
  return (
    <AbsoluteFill style={{ opacity: v }}>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 26%)" }} />
      <div style={{ position: "absolute", top: 120, left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{ transform: `scale(${tile}) rotate(${(1 - tile) * -90}deg)`, background: PAPER, borderRadius: 30, padding: 14, boxShadow: cardShadow }}>
            <ClaudeMark size={92} rotate={frame * 0.6} />
          </div>
          <div style={{ transform: `translateX(${(1 - band) * 900}px)`, background: ACCENT, borderRadius: 24, padding: "6px 40px 14px", boxShadow: cardShadow }}>
            <span style={{ fontFamily: SANS, fontWeight: 900, fontSize: 100, color: "#fff", letterSpacing: -3 }}>
              Claude <Italic size={118}>Apps</Italic>
            </span>
          </div>
        </div>
        <div style={{ position: "relative", height: 70 }}>
          <div style={{ position: "absolute", left: "50%", transform: `translateX(-50%) scale(${nou * (1 - free)})`, whiteSpace: "nowrap", background: "#fff", color: INK, borderRadius: 999, padding: "10px 28px", fontFamily: SANS, fontWeight: 900, fontSize: 38 }}>⚡ NOU de la Anthropic</div>
          <div style={{ position: "absolute", left: "50%", transform: `translateX(-50%) scale(${free})`, whiteSpace: "nowrap", background: "#1F9D55", color: "#fff", borderRadius: 999, padding: "10px 28px", fontFamily: SANS, fontWeight: 900, fontSize: 38 }}>✓ Merge și pe planul gratuit</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Sticker: React.FC<{ at: number; children: React.ReactNode }> = ({ at, children }) => {
  const { frame, fps, out } = useScene(6);
  const s = pop(frame, at, fps);
  return (
    <div style={{ position: "absolute", top: 140, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: out }}>
      <div style={{ transform: `scale(${s}) rotate(-2deg)`, opacity: Math.min(1, s * 2) }}>{children}</div>
    </div>
  );
};

const Simple: React.FC = () => (
  <Sticker at={rel(S.simple.kid, S.simple.start)}>
    <div style={{ background: PAPER, borderRadius: 30, padding: "18px 36px", boxShadow: cardShadow, fontFamily: SANS, fontWeight: 900, fontSize: 50, color: INK, display: "flex", alignItems: "center", gap: 16 }}>
      👶 Simplu, <Italic size={62} color={ACCENT}>chiar și la 5 ani</Italic>
    </div>
  </Sticker>
);

const CTA: React.FC = () => (
  <Sticker at={rel(S.cta.comments, S.cta.start) - 4}>
    <div style={{ background: PAPER, borderRadius: 34, padding: "22px 40px", boxShadow: cardShadow, fontFamily: SANS, color: INK, display: "flex", alignItems: "center", gap: 22 }}>
      <span style={{ fontSize: 84 }}>💬</span>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <span style={{ fontWeight: 900, fontSize: 46 }}>Scrie-mi în comentarii</span>
        <Italic size={56} color={ACCENT}>ce aplicație ai creat?</Italic>
      </div>
    </div>
  </Sticker>
);

const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const st = S.outro.start;
  const l1 = pop(frame, rel(S.outro.digital, st) - 3, fps);
  const l2 = pop(frame, rel(S.outro.geo, st) - 3, fps);
  const wakeAt = rel(S.outro.wake, st);
  const wake = spring({ frame: frame - wakeAt, fps, config: { damping: 12, stiffness: 160 } });
  const ro = spring({ frame: frame - rel(S.outro.ro, st), fps, config: { damping: 9, stiffness: 180, mass: 0.7 } });
  const band = interpolate(frame, [wakeAt, wakeAt + 12], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const shade = interpolate(frame, [0, 8], [0, 1], clamp);
  const end = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0.0], clamp);
  const line: React.CSSProperties = { fontFamily: SANS, fontWeight: 900, fontSize: 86, color: "#fff", letterSpacing: -2, textShadow: "0 5px 22px rgba(0,0,0,.6)", lineHeight: 1.05 };
  return (
    <AbsoluteFill style={{ opacity: end }}>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 52%, rgba(0,0,0,0.8) 82%)", opacity: shade }} />
      <div style={{ position: "absolute", left: 60, right: 60, top: 1170, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
        <div style={{ display: "flex", gap: 30, transform: `scale(${1 - 0.1 * wake})` }}>
          <div style={{ ...line, opacity: l1, transform: `translateY(${(1 - l1) * 40}px)` }}>
            Fii <Italic size={104} color={ACCENT}>digital.</Italic>
          </div>
          <div style={{ ...line, opacity: l2, transform: `translateY(${(1 - l2) * 40}px)` }}>
            Fii <Italic size={104} color={ACCENT}>GEO.</Italic>
          </div>
        </div>
        <div style={{ ...line, fontSize: 112, opacity: wake, transform: `translateY(${(1 - wake) * 70}px)`, marginTop: 8 }}>Deșteaptă-te,</div>
        <div style={{ ...line, fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, fontSize: 150, letterSpacing: 0, opacity: ro, transform: `scale(${0.6 + 0.4 * ro})` }}>române!</div>
        <div style={{ display: "flex", width: 520 * band, height: 16, borderRadius: 8, overflow: "hidden", marginTop: 6 }}>
          <div style={{ flex: 1, background: "#002B7F" }} />
          <div style={{ flex: 1, background: "#FCD116" }} />
          <div style={{ flex: 1, background: "#CE1126" }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ============================================================ exports */
const B = Object.fromEntries((TL.blocks as { name: string; start: number; end: number }[]).map((b) => [b.name, b]));

export const PanelGraphics: React.FC = () => (
  <AbsoluteFill>
    <At name="① chapter" start={B.ideas.start} end={B.share.end}>
      <Chapter n="1" label="IDEI DE APLICAȚII" />
    </At>
    <At name="2 idei" start={S.ideas.start} end={S.ideas.end}>
      <Ideas />
    </At>
    <At name="Ideea #1" start={S.app1.start} end={S.app1.end}>
      <App1 />
    </At>
    <At name="Ideea #2" start={S.app2.start} end={S.app2.end}>
      <App2 />
    </At>
    <At name="Notificare" start={S.notif.start} end={S.notif.end}>
      <Notif />
    </At>
    <At name="Share" start={S.share.start} end={S.share.end}>
      <Share />
    </At>
    <At name="② chapter" start={B.how_prompt.start} end={B.recap.end}>
      <Chapter n="2" label="CUM O FACI" />
    </At>
    <At name="3 pași" start={S.how.start} end={S.how.end}>
      <How />
    </At>
    <At name="Recap" start={S.recap.start} end={S.recap.end}>
      <Recap />
    </At>
  </AbsoluteFill>
);

export const FullGraphics: React.FC = () => (
  <AbsoluteFill>
    <At name="HOOK" start={S.hook.start} end={S.hook.end}>
      <Hook />
    </At>
    <At name="Simplu" start={S.simple.start} end={S.simple.end}>
      <Simple />
    </At>
    <At name="CTA" start={S.cta.start} end={S.cta.end}>
      <CTA />
    </At>
    <At name="Outro" start={S.outro.start} end={S.outro.end}>
      <Outro />
    </At>
  </AbsoluteFill>
);
