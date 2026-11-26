import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";
import timeline from "./data/timeline.json";

const LATIN = "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const LATIN_EXT = "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1E00-1E9F, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF";

// Fonts are served locally (public/fonts) so rendering works offline.
export const SANS = "Inter";
export const SERIF = "Instrument Serif";
for (const [file, range] of [["inter-latin", LATIN], ["inter-latinext", LATIN_EXT]] as const) {
  loadFont({ family: SANS, url: staticFile(`fonts/${file}.woff2`), weight: "100 900", unicodeRange: range });
}
for (const [file, range] of [["serif-latin", LATIN], ["serif-latinext", LATIN_EXT]] as const) {
  loadFont({ family: SERIF, url: staticFile(`fonts/${file}.woff2`), style: "italic", weight: "400", unicodeRange: range });
}

export const TL = timeline;
export const FPS = timeline.fps;
export const ACCENT = "#D97757";
export const INK = "#1F1E1D";
export const PAPER = "#FAF9F5";

/** seconds -> frames */
export const f = (s: number) => Math.round(s * FPS);

export const cardShadow =
  "0 40px 90px rgba(0,0,0,0.40), 0 10px 24px rgba(0,0,0,0.22)";
