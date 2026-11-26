import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';
import {CasualMan} from './components/CasualMan';
import {WingedBoy} from './components/WingedBoy';
import {ExpressionName} from './kit/expressions';

/**
 * FaceLab — one character, head-on, one expression per render.
 * A close-up camera on the head so each face reads clearly at full size.
 * The expression is a composition prop (pass it as inputProps when
 * rendering stills), so one composition covers all 27 expressions.
 *
 * Default: BoltBoy, 'grin' (his original face) — the regression check
 * that the expression wiring did not change the default look.
 */
export const FaceLab: React.FC<{
  character?: 'boltboy' | 'casualman' | 'wingedboy';
  expression?: ExpressionName;
  expressionT?: number;
}> = ({character = 'boltboy', expression = 'grin', expressionT = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <Stage cameraPosition={[0, 5.2, 6]} lookAt={[0, 5.2, 0]} fov={30}>
      {character === 'boltboy' ? (
        <BoltBoy t={t} walk={0} expression={expression} expressionT={expressionT} position={[0, 0, 0]} />
      ) : character === 'casualman' ? (
        <CasualMan t={t} walk={0} expression={expression} expressionT={expressionT} position={[0, 0, 0]} />
      ) : (
        <WingedBoy t={t} walk={0} expression={expression} expressionT={expressionT} position={[0, 0, 0]} />
      )}
    </Stage>
  );
};
