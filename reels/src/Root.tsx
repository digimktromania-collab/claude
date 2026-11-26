import { Composition } from "remotion";
import { TL } from "./lib";
import { Main } from "./Main";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ClaudeAppsReel"
      component={Main}
      durationInFrames={TL.durationInFrames}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
