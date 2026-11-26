import React from "react";
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
import { AppleLogo, ClaudeMark, WindowsLogo } from "./Logos";
import { ACCENT, cardShadow, f, INK, PAPER, SANS, SERIF, TL } from "./lib";

/** Big centre text on the install step. The voice says "click pe cele trei butoane". */
export const BIG_CLICK_TEXT = "CLICK ⋯";

const S = TL.scenes;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** Wraps a graphic in a Sequence placed on absolute seconds (output timeline). */
const At: React.FC<{ start: number; end: number; name: string; children: React.ReactNode }> = ({
  start,
  end,
  name,
  children,
}) => (
  <Sequence name={name} from={f(start)} durationInFrames={Math.max(1, f(end) - f(start))} premountFor={30}>
    {children}
  </Sequence>
);

/** enter spring (0..1) and exit (1..0) for the current Sequence */
const useInOut = (exitFrames = 7) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 16, stiffness: 180, mass: 0.8 } });
  const exit = interpolate(frame, [durationInFrames - exitFrames, durationInFrames], [1, 0], clamp);
  return { frame, fps, enter, exit, v: Math.min(enter, exit) };
};

/** local frame at which an absolute time happens inside a scene */
const rel = (abs: number, sceneStart: number) => f(abs) - f(sceneStart);

const pop = (frame: number, at: number, fps: number) =>
  spring({ frame: frame - at, fps, config: { damping: 11, stiffness: 220, mass: 0.6 } });

const slideUp = (v: number, dist = 140): React.CSSProperties => ({
  transform: `translateY(${(1 - v) * dist}px)`,
  opacity: Math.min(1, v * 1.4),
});

const Card: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div
    style={{
      background: PAPER,
      borderRadius: 44,
      boxShadow: cardShadow,
      padding: "40px 48px",
      color: INK,
      fontFamily: SANS,
      ...style,
    }}
  >
    {children}
  </div>
);

const TopZone: React.FC<{ children: React.ReactNode; top?: number }> = ({ children, top = 150 }) => (
  <div style={{ position: "absolute", left: 60, right: 60, top, display: "flex", flexDirection: "column", alignItems: "center" }}>
    {children}
  </div>
);

/* ------------------------------------------------------------------ HOOK */
const Hook: React.FC = () => {
  const { frame, fps, v } = useInOut(6);
  const logo = pop(frame, 0, fps);
  const band = spring({ frame: frame - 4, fps, config: { damping: 18, stiffness: 150 } });
  const pill = pop(frame, 12, fps);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 42%)", opacity: v }} />
      <TopZone top={210}>
        <div style={{ opacity: v, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
          <div style={{ transform: `scale(${logo}) rotate(${(1 - logo) * -120}deg)` }}>
            <div style={{ background: PAPER, borderRadius: 48, padding: 26, boxShadow: cardShadow }}>
              <ClaudeMark size={150} rotate={frame * 0.6} />
            </div>
          </div>
          <div
            style={{
              background: ACCENT,
              padding: "18px 56px 24px",
              borderRadius: 22,
              transform: `translateX(${(1 - band) * -1100}px) rotate(-2deg)`,
              boxShadow: cardShadow,
            }}
          >
            <span style={{ fontFamily: SANS, fontWeight: 900, fontSize: 128, color: "#fff", letterSpacing: -4 }}>
              Claude{" "}
              <span style={{ fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, letterSpacing: 0, fontSize: 150 }}>Apps</span>
            </span>
          </div>
          <div
            style={{
              transform: `scale(${pill})`,
              background: "#fff",
              color: INK,
              fontFamily: SANS,
              fontWeight: 800,
              fontSize: 40,
              padding: "12px 30px",
              borderRadius: 999,
              boxShadow: cardShadow,
            }}
          >
            ⚡ Vestea zilei în AI
          </div>
        </div>
      </TopZone>
    </AbsoluteFill>
  );
};

/* ----------------------------------------------------------------- PLANS */
const Plans: React.FC = () => {
  const { frame, fps, v } = useInOut(5);
  const plans = ["Free", "Pro", "Max", "Team"];
  const circleAt = rel(S.plans.free, S.plans.start);
  const draw = interpolate(frame, [circleAt, circleAt + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <TopZone top={200}>
      <div style={{ ...slideUp(v), display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
        <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 64, color: "#fff", textShadow: "0 4px 18px rgba(0,0,0,.6)" }}>
          Toate <span style={{ fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, fontSize: 80 }}>planurile</span>
        </div>
        <div style={{ display: "flex", gap: 22 }}>
          {plans.map((p, i) => {
            const s = pop(frame, i * 3, fps);
            const isFree = i === 0;
            return (
              <div key={p} style={{ position: "relative", transform: `scale(${s})` }}>
                <div
                  style={{
                    background: isFree ? ACCENT : PAPER,
                    color: isFree ? "#fff" : INK,
                    fontFamily: SANS,
                    fontWeight: 900,
                    fontSize: 54,
                    padding: "22px 36px",
                    borderRadius: 26,
                    boxShadow: cardShadow,
                  }}
                >
                  {p}
                </div>
                {isFree ? (
                  <svg width={260} height={170} viewBox="0 0 260 170" style={{ position: "absolute", left: -38, top: -30, overflow: "visible" }}>
                    <ellipse
                      cx={130}
                      cy={85}
                      rx={118}
                      ry={72}
                      fill="none"
                      stroke="#fff"
                      strokeWidth={9}
                      strokeLinecap="round"
                      pathLength={1}
                      strokeDasharray={1}
                      strokeDashoffset={1 - draw}
                      transform="rotate(-6 130 85)"
                    />
                  </svg>
                ) : null}
              </div>
            );
          })}
        </div>
      </div>
    </TopZone>
  );
};

/* ------------------------------------------------- WINDOW + ICON (infographic) */
const WindowInfographic: React.FC = () => {
  const { frame, fps, v } = useInOut(6);
  const iconAt = rel(S.window.icon, S.window.start);
  const icon = pop(frame, iconAt, fps);
  return (
    <TopZone top={170}>
      <div style={{ ...slideUp(v), position: "relative", width: 860, height: 560 }}>
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: 760,
            height: 480,
            background: PAPER,
            borderRadius: 30,
            boxShadow: cardShadow,
            overflow: "hidden",
          }}
        >
          <div style={{ height: 70, background: "#EDE9DF", display: "flex", alignItems: "center", padding: "0 26px", gap: 14 }}>
            {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => (
              <div key={c} style={{ width: 22, height: 22, borderRadius: 11, background: c }} />
            ))}
            <div style={{ marginLeft: 22, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: INK }}>Photo Resizer</div>
          </div>
          <div style={{ display: "flex", padding: 30, gap: 30 }}>
            <div style={{ width: 200, display: "flex", flexDirection: "column", gap: 18 }}>
              {[180, 140, 160, 120].map((w, i) => (
                <div key={i} style={{ width: w * Math.min(1, Math.max(0, (frame - 6 - i * 2) / 8)), height: 22, borderRadius: 11, background: "#E3DED2" }} />
              ))}
            </div>
            <div style={{ flex: 1, height: 330, borderRadius: 20, background: "#F0ECE3", display: "flex", alignItems: "center", justifyContent: "center", gap: 18 }}>
              {["1:1", "9:16", "4:5"].map((r, i) => (
                <div
                  key={r}
                  style={{
                    width: [110, 80, 96][i],
                    height: [110, 150, 120][i],
                    borderRadius: 12,
                    background: i === 1 ? ACCENT : "#D9D3C5",
                    color: "#fff",
                    fontFamily: SANS,
                    fontWeight: 800,
                    fontSize: 24,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    transform: `scale(${pop(frame, 8 + i * 3, fps)})`,
                  }}
                >
                  {r}
                </div>
              ))}
            </div>
          </div>
        </div>
        {/* app icon */}
        <div style={{ position: "absolute", right: 0, bottom: 0, transform: `scale(${icon}) rotate(${(1 - icon) * 30}deg)`, display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
          <div style={{ width: 200, height: 200, borderRadius: 50, background: `linear-gradient(145deg, #E88B6B, ${ACCENT})`, boxShadow: cardShadow, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <ClaudeMark size={120} color="#fff" />
          </div>
        </div>
        <div style={{ position: "absolute", left: 20, bottom: -14, opacity: icon, fontFamily: SANS, fontWeight: 800, fontSize: 40, color: "#fff", textShadow: "0 3px 14px rgba(0,0,0,.7)" }}>
          fereastra ei + <span style={{ fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, fontSize: 52 }}>iconiță</span>
        </div>
      </div>
    </TopZone>
  );
};

/* ------------------------------------------------------ PROMPT CARDS */
const Typewriter: React.FC<{ text: string; startFrame: number; cps: number; size?: number }> = ({ text, startFrame, cps, size = 50 }) => {
  const frame = useCurrentFrame();
  const n = Math.max(0, Math.min(text.length, Math.floor((frame - startFrame) * cps)));
  const caretOn = Math.floor(frame / 8) % 2 === 0 || n < text.length;
  return (
    <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: size, lineHeight: 1.28, color: INK, minHeight: size * 1.28 }}>
      {text.slice(0, n)}
      <span style={{ display: "inline-block", width: 5, height: size * 0.95, marginLeft: 4, verticalAlign: "-0.12em", background: ACCENT, opacity: caretOn ? 1 : 0 }} />
    </div>
  );
};

const PromptCard: React.FC<{
  label: string;
  icon: string;
  prompt: string;
  sceneStart: number;
  sceneEnd: number;
  footer?: React.ReactNode;
}> = ({ label, icon, prompt, sceneStart, sceneEnd, footer }) => {
  const { frame, fps, v } = useInOut(7);
  const iconPop = pop(frame, 5, fps);
  const dur = f(sceneEnd) - f(sceneStart);
  const cps = Math.min(1.6, prompt.length / (dur * 0.6));
  return (
    <TopZone top={150}>
      <div style={{ ...slideUp(v, 180), width: "100%" }}>
        <Card style={{ padding: "34px 44px 40px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 22, marginBottom: 22 }}>
            <div
              style={{
                width: 96,
                height: 96,
                borderRadius: 28,
                background: "#FBEDE6",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 58,
                transform: `scale(${iconPop}) rotate(${(1 - iconPop) * -25}deg)`,
              }}
            >
              {icon}
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <span style={{ fontWeight: 900, fontSize: 46, letterSpacing: -1 }}>{label}</span>
              <span style={{ fontWeight: 600, fontSize: 28, color: "#8A8478" }}>Prompt pentru Claude</span>
            </div>
          </div>
          <div style={{ background: "#fff", border: "3px solid #ECE7DC", borderRadius: 26, padding: "24px 30px" }}>
            <Typewriter text={prompt} startFrame={8} cps={cps} />
          </div>
          {footer}
        </Card>
      </div>
    </TopZone>
  );
};

const DesktopFooter: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const at = rel(S.platforms.start, S.card1.start);
  const a = pop(frame, at, fps);
  const b = pop(frame, at + 4, fps);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 26, marginTop: 26, opacity: Math.min(1, a * 2) }}>
      <div style={{ transform: `scale(${a})` }}>
        <AppleLogo size={70} />
      </div>
      <span style={{ fontWeight: 900, fontSize: 44, transform: `scale(${a})` }}>Mac</span>
      <span style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 50, color: "#8A8478" }}>și</span>
      <div style={{ transform: `scale(${b})` }}>
        <WindowsLogo size={62} />
      </div>
      <span style={{ fontWeight: 900, fontSize: 44, transform: `scale(${b})` }}>Windows</span>
    </div>
  );
};

const StepsFooter: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const steps = ["Scrie promptul", "Trimite-l lui Claude", "Claude lucrează în artefact"];
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14, marginTop: 26 }}>
      {steps.map((s, i) => {
        const at = rel(S.card3.steps[i], S.card3.start);
        const p = pop(frame, at, fps);
        return (
          <div key={s} style={{ display: "flex", alignItems: "center", gap: 20, opacity: Math.min(1, p * 2), transform: `translateX(${(1 - p) * 60}px)` }}>
            <div style={{ width: 58, height: 58, borderRadius: 29, background: ACCENT, color: "#fff", fontWeight: 900, fontSize: 32, display: "flex", alignItems: "center", justifyContent: "center" }}>
              {i + 1}
            </div>
            <span style={{ fontWeight: 800, fontSize: 42 }}>{s}</span>
          </div>
        );
      })}
    </div>
  );
};

/* ---------------------------------------------- FEATURES: 🔔 🖥️ ⌨️ */
const Features: React.FC = () => {
  const { frame, fps, v } = useInOut(5);
  const items = [
    { e: "🔔", l: "Notificări", at: S.features.bell },
    { e: "🖥️", l: "Bara de meniu", at: S.features.menu },
    { e: "⌨️", l: "Scurtături", at: S.features.keys },
  ];
  return (
    <TopZone top={210}>
      <div style={{ display: "flex", gap: 26, opacity: v }}>
        {items.map((it, i) => {
          const p = pop(frame, rel(it.at, S.features.start), fps);
          const ring = i === 0 ? Math.sin(Math.max(0, frame - rel(it.at, S.features.start)) * 0.9) * 14 * Math.max(0, 1 - (frame - rel(it.at, S.features.start)) / 20) : 0;
          return (
            <div key={it.l} style={{ transform: `scale(${p}) translateY(${(1 - p) * 60}px)`, opacity: Math.min(1, p * 2) }}>
              <Card style={{ width: 290, padding: "34px 10px 30px", display: "flex", flexDirection: "column", alignItems: "center", gap: 16 }}>
                <div style={{ fontSize: 120, transform: `rotate(${ring}deg)` }}>{it.e}</div>
                <div style={{ fontWeight: 900, fontSize: 38, textAlign: "center", letterSpacing: -0.5 }}>{it.l}</div>
              </Card>
            </div>
          );
        })}
      </div>
    </TopZone>
  );
};

/* ------------------------------------------------------------ WARNING */
const Warning: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const bg = interpolate(frame, [0, 6, durationInFrames - 8, durationInFrames], [0, 1, 1, 0], clamp);
  const red = spring({ frame, fps, config: { damping: 13, stiffness: 170 } });
  const greenAt = rel(S.warning.green, S.warning.start);
  const green = spring({ frame: frame - greenAt, fps, config: { damping: 13, stiffness: 170 } });
  const shake = frame < 14 ? Math.sin(frame * 2.2) * (14 - frame) * 0.9 : 0;
  const out = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], clamp);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, rgba(28,20,20,0.92), rgba(5,5,7,0.97))", opacity: bg }} />
      <div style={{ position: "absolute", top: 230, left: 0, right: 0, textAlign: "center", opacity: bg, fontFamily: SANS, fontWeight: 900, fontSize: 52, letterSpacing: 8, color: "#FF6B6B" }}>
        ⚠️ ATENȚIE
      </div>
      <div style={{ position: "absolute", left: 80, right: 80, top: 360, ...slideUp(red, 200), opacity: Math.min(red, out), transform: `translateY(${(1 - red) * 200}px) translateX(${shake}px)` }}>
        <div style={{ background: "#D93A3A", borderRadius: 40, padding: "46px 50px", boxShadow: "0 40px 100px rgba(217,58,58,0.45)", color: "#fff", fontFamily: SANS }}>
          <div style={{ fontSize: 84, marginBottom: 6 }}>🛑</div>
          <div style={{ fontWeight: 900, fontSize: 70, lineHeight: 1.08, letterSpacing: -1.5 }}>
            Anthropic <span style={{ fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, fontSize: 84 }}>nu verifică</span> aplicațiile
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 80, right: 80, top: 820, opacity: Math.min(green * 1.4, out), transform: `translateY(${(1 - green) * 220}px)` }}>
        <div style={{ background: "#1F9D55", borderRadius: 40, padding: "46px 50px", boxShadow: "0 40px 100px rgba(31,157,85,0.45)", color: "#fff", fontFamily: SANS }}>
          <div style={{ fontSize: 84, marginBottom: 6 }}>✅</div>
          <div style={{ fontWeight: 900, fontSize: 70, lineHeight: 1.08, letterSpacing: -1.5 }}>
            Dă-i doar <span style={{ fontFamily: SERIF, fontStyle: "italic", fontWeight: 400, fontSize: 84 }}>permisiunile</span> necesare
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ----------------------------------------------------- INSTALL STEPS */
const Install: React.FC = () => {
  const { frame, fps, v } = useInOut(7);
  const W = 960;
  const k = W / 860; // png native width 860x640
  const clickAt = rel(S.install.click, S.install.start);
  const dotsAt = rel(S.install.dots, S.install.start);
  const ulAt = rel(S.install.underline, S.install.start);
  const circle = interpolate(frame, [dotsAt, dotsAt + 9], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const marker = interpolate(frame, [ulAt, ulAt + 10], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const big = spring({ frame: frame - clickAt, fps, config: { damping: 9, stiffness: 200, mass: 0.7 } });
  const bigOut = interpolate(frame, [clickAt + 34, clickAt + 42], [1, 0], clamp);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: (1080 - W) / 2, top: 400, width: W, height: 640 * k, ...slideUp(v, 260) }}>
        <Img
          src={staticFile("assets/install-steps.png")}
          style={{ width: W, height: 640 * k, borderRadius: 36 * k, boxShadow: "0 50px 110px rgba(0,0,0,0.5), 0 14px 30px rgba(0,0,0,0.25)" }}
        />
        <svg width={W} height={640 * k} viewBox="0 0 860 640" style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          {/* circle around ⋯ */}
          <ellipse cx={749} cy={97} rx={70} ry={52} fill="none" stroke={ACCENT} strokeWidth={7} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - circle} transform="rotate(-8 749 97)" />
          {/* marker underline under "Install as app" */}
          <path d="M 380 512 C 450 506, 540 516, 612 508" fill="none" stroke={ACCENT} strokeWidth={13} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - marker} opacity={0.95} />
        </svg>
      </div>
      {frame >= clickAt ? (
        <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", opacity: bigOut }}>
          <div
            style={{
              transform: `scale(${big}) rotate(-5deg)`,
              background: INK,
              color: "#fff",
              fontFamily: SANS,
              fontWeight: 900,
              fontSize: 150,
              letterSpacing: -4,
              padding: "10px 50px 22px",
              borderRadius: 30,
              border: `8px solid ${ACCENT}`,
              boxShadow: cardShadow,
            }}
          >
            {BIG_CLICK_TEXT}
          </div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ CTA */
const CTA: React.FC = () => {
  const { frame, fps, enter } = useInOut(1);
  const comAt = rel(S.cta.comments, S.cta.start);
  const bump = pop(frame, comAt, fps);
  const pulse = 1 + 0.035 * Math.sin(frame / 6);
  return (
    <TopZone top={190}>
      <div style={{ ...slideUp(enter, 200) }}>
        <Card style={{ display: "flex", alignItems: "center", gap: 30, padding: "36px 46px", transform: `scale(${pulse})` }}>
          <div style={{ fontSize: 110, transform: `scale(${0.8 + 0.2 * bump}) rotate(${(1 - bump) * 20}deg)` }}>💬</div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <span style={{ fontWeight: 900, fontSize: 64, letterSpacing: -1.5 }}>
              Scrie{" "}
              <span style={{ background: ACCENT, color: "#fff", padding: "0 18px", borderRadius: 16 }}>APP</span>
            </span>
            <span style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 74, lineHeight: 1.05 }}>în comentarii</span>
          </div>
        </Card>
      </div>
    </TopZone>
  );
};

export const Scenes: React.FC = () => {
  return (
    <AbsoluteFill>
      <At name="HOOK" start={S.hook.start} end={S.hook.end}>
        <Hook />
      </At>
      <At name="Toate planurile" start={S.plans.start} end={S.plans.end}>
        <Plans />
      </At>
      <At name="Fereastră + iconiță" start={S.window.start} end={S.window.end}>
        <WindowInfographic />
      </At>
      <At name="Card 1 (resize poze)" start={S.card1.start} end={S.card1.end}>
        <PromptCard label={S.card1.label} icon={S.card1.icon} prompt={S.card1.prompt} sceneStart={S.card1.start} sceneEnd={S.card1.end} footer={<DesktopFooter />} />
      </At>
      <At name="Card 2 (reminder TikTok)" start={S.card2.start} end={S.card2.end}>
        <PromptCard label={S.card2.label} icon={S.card2.icon} prompt={S.card2.prompt} sceneStart={S.card2.start} sceneEnd={S.card2.end} />
      </At>
      <At name="Notificări / meniu / scurtături" start={S.features.start} end={S.features.end}>
        <Features />
      </At>
      <At name="AVERTISMENT" start={S.warning.start} end={S.warning.end}>
        <Warning />
      </At>
      <At name="Card 3 (pașii)" start={S.card3.start} end={S.card3.end}>
        <PromptCard label={S.card3.label} icon={S.card3.icon} prompt={S.card3.prompt} sceneStart={S.card3.start} sceneEnd={S.card3.end} footer={<StepsFooter />} />
      </At>
      <At name="Install as app" start={S.install.start} end={S.install.end}>
        <Install />
      </At>
      <At name="CTA" start={S.cta.start} end={S.cta.end}>
        <CTA />
      </At>
    </AbsoluteFill>
  );
};
