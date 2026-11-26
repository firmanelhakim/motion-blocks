import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, timelinePose, Performance} from './kit/kit';
import {performanceFace} from './kit/expressions';
import {BoltBoy} from './components/BoltBoy';

/**
 * PerformanceLab — the two-lane Performance timeline: a face track and a
 * body track running in parallel, each with its own timing. Face and body
 * are independent — any expression over any pose — and both crossfade
 * (smoothstep, 0.25s) at their own segment boundaries.
 *
 * Demo "Greeting" (8s loop, BoltBoy):
 *   body: wave 2s -> bow 1.6s -> cheer 1.6s -> idle 2.8s
 *   face: smile 2s -> proud 1.6s -> excited 1.6s -> laugh 2.8s
 * The lanes are in step (both total 8s) but they don't have to be: a face
 * can change mid-pose, and a pose can change mid-expression.
 */
export const GREETING_PERFORMANCE: Performance = {
  face: [
    {expression: 'smile', duration: 2},
    {expression: 'proud', duration: 1.6},
    {expression: 'excited', duration: 1.6},
    {expression: 'laugh', duration: 2.8},
  ],
  body: [
    {clip: 'wave', duration: 2},
    {clip: 'bow', duration: 1.6},
    {clip: 'cheer', duration: 1.6},
    {clip: 'idle', duration: 2.8},
  ],
};

export const PerformanceLab: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const body = timelinePose(GREETING_PERFORMANCE.body, t);
  const face = performanceFace(GREETING_PERFORMANCE.face, t);
  return (
    <Stage shadows>
      <BoltBoy pose={body.pose} faceState={face} expressionT={t} />
    </Stage>
  );
};
