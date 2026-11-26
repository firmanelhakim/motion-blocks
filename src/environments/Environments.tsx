import React from 'react';
import { HouseVariantId, LocationId } from '../types/schema';
import { ScienceFx } from '../types/schema';
import { LOCATION_INFO } from './locations';
import { TownExterior } from './town/TownMap';
import { BeachEnvironment } from './beach';
import { SpaceEnvironment } from './space';
import { MarsEnvironment } from './mars';
import { TunnelEnvironment } from './tunnel';
import { UnderseaEnvironment } from './undersea';
import { DrySeabedEnvironment } from './dryseabed';
import { IceStreetEnvironment } from './ice-street';
import { StudioEnvironment } from './studio';
import {
  BedroomEnvironment,
  ClassroomEnvironment,
  HallwayEnvironment,
  KitchenEnvironment,
  LivingRoomEnvironment,
} from './interiors';

/** Picks the 3D set for a scene. Exteriors are anchors into one shared town map. */
export const EnvironmentSwitch: React.FC<{
  location: LocationId;
  isNight?: boolean;
  blackout?: boolean;
  variant?: HouseVariantId;
  boardText?: string[];
  schoolName?: string;
  fx?: ScienceFx[];
}> = ({ location, isNight = false, blackout = false, variant = 'blue', boardText, schoolName, fx }) => {
  // Unknown locations used to fall through to TownExterior silently, so a
  // typo in generated story data rendered the wrong set with no error.
  // Every valid location is in LOCATION_INFO; anything else is a bug.
  if (!(location in LOCATION_INFO)) {
    throw new Error(
      `EnvironmentSwitch: unknown location "${String(location)}" — expected one of: ${Object.keys(LOCATION_INFO).join(', ')}.`
    );
  }
  switch (location) {
    case 'classroom':
      return <ClassroomEnvironment night={isNight} boardText={boardText} fx={fx} />;
    case 'hallway':
      return <HallwayEnvironment night={isNight} fx={fx} />;
    case 'living_room':
      return <LivingRoomEnvironment variant={variant} night={isNight} fx={fx} />;
    case 'kitchen':
      return <KitchenEnvironment variant={variant} night={isNight} fx={fx} />;
    case 'bedroom':
      return <BedroomEnvironment variant={variant} night={isNight} fx={fx} />;
    case 'beach':
      return <BeachEnvironment night={isNight} fx={fx} />;
    case 'space':
      return <SpaceEnvironment fx={fx} />;
    case 'mars':
      return <MarsEnvironment fx={fx} />;
    case 'tunnel':
      return <TunnelEnvironment fx={fx} />;
    case 'undersea':
      return <UnderseaEnvironment fx={fx} />;
    case 'dryseabed':
      return <DrySeabedEnvironment fx={fx} />;
    case 'ice_street':
      return <IceStreetEnvironment fx={fx} />;
    case 'studio':
      return <StudioEnvironment variant={variant} fx={fx} />;
    default:
      return <TownExterior location={location} variant={variant} night={isNight} blackout={blackout} schoolName={schoolName} fx={fx} />;
  }
};
