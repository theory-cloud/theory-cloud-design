/**
 * Theory Cloud — exported token contract.
 *
 * This local structural type keeps the published design package free of a
 * hard FaceTheory dependency. FaceTheory compatibility is still enforced by
 * `contracts/facetheory-stitch-token-set.ts`, which checks these tokens
 * against the latest pinned FaceTheory validation baseline during `npm run
 * check`.
 */

export type TheoryCloudColorValue = string;

export interface TheoryCloudPaletteTokens {
  primary: TheoryCloudColorValue;
  primaryContainer: TheoryCloudColorValue;
  primaryFixed: TheoryCloudColorValue;
  primaryFixedDim: TheoryCloudColorValue;
  onPrimary: TheoryCloudColorValue;
  onPrimaryContainer: TheoryCloudColorValue;
  onPrimaryFixed: TheoryCloudColorValue;
  onPrimaryFixedVariant: TheoryCloudColorValue;
  inversePrimary: TheoryCloudColorValue;
  surfaceTint: TheoryCloudColorValue;

  secondary: TheoryCloudColorValue;
  secondaryContainer: TheoryCloudColorValue;
  secondaryFixed: TheoryCloudColorValue;
  secondaryFixedDim: TheoryCloudColorValue;
  onSecondary: TheoryCloudColorValue;
  onSecondaryContainer: TheoryCloudColorValue;
  onSecondaryFixed: TheoryCloudColorValue;
  onSecondaryFixedVariant: TheoryCloudColorValue;

  tertiary: TheoryCloudColorValue;
  tertiaryContainer: TheoryCloudColorValue;
  tertiaryFixed: TheoryCloudColorValue;
  tertiaryFixedDim: TheoryCloudColorValue;
  onTertiary: TheoryCloudColorValue;
  onTertiaryContainer: TheoryCloudColorValue;
  onTertiaryFixed: TheoryCloudColorValue;
  onTertiaryFixedVariant: TheoryCloudColorValue;

  background: TheoryCloudColorValue;
  surface: TheoryCloudColorValue;
  surfaceBright: TheoryCloudColorValue;
  surfaceDim: TheoryCloudColorValue;
  surfaceContainerLowest: TheoryCloudColorValue;
  surfaceContainerLow: TheoryCloudColorValue;
  surfaceContainer: TheoryCloudColorValue;
  surfaceContainerHigh: TheoryCloudColorValue;
  surfaceContainerHighest: TheoryCloudColorValue;
  surfaceVariant: TheoryCloudColorValue;

  inverseSurface: TheoryCloudColorValue;
  inverseOnSurface: TheoryCloudColorValue;

  onBackground: TheoryCloudColorValue;
  onSurface: TheoryCloudColorValue;
  onSurfaceVariant: TheoryCloudColorValue;

  outline: TheoryCloudColorValue;
  outlineVariant: TheoryCloudColorValue;

  error: TheoryCloudColorValue;
  errorContainer: TheoryCloudColorValue;
  onError: TheoryCloudColorValue;
  onErrorContainer: TheoryCloudColorValue;
}

export interface TheoryCloudTypographyTokens {
  displayFont: string;
  bodyFont: string;
  labelFont: string;
}

export interface TheoryCloudRoundnessTokens {
  sm: number;
  md: number;
  lg: number;
  xl: number;
}

export interface TheoryCloudSpacingTokens {
  baseUnit: number;
}

export interface TheoryCloudTokenSet {
  mode: "dark";
  palette: TheoryCloudPaletteTokens;
  typography: TheoryCloudTypographyTokens;
  roundness: TheoryCloudRoundnessTokens;
  spacing: TheoryCloudSpacingTokens;
}
