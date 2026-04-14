# bootc Templates for Socios Immutable Nodes

This directory contains the first bootc-oriented skeleton for the Socios immutable host lane.

The contents here are intentionally minimal and are meant to anchor the standards posture rather than define a final production image.

## Purpose

This directory exists to make the immutable-node standards concrete:

- the host is composed as an image, not assembled through drift;
- critical host services are image-baked;
- critical service images can be lifecycle-coupled to the host;
- `/var` remains the durable mutable state plane.

## Contents

- `Containerfile.example` — illustrative base image composition pattern for a Socios immutable node.

## Notes

1. The example Containerfile is not final production packaging.
2. Placeholder image names and commands MUST be replaced during realization.
3. The reference shape here is bootc-first but intended to remain conceptually OSTree-compatible.
4. Critical services should be represented both as Quadlet units and, where appropriate, as bound-image references.

## Expected follow-on work

- replace placeholder base image references;
- add concrete host helper binaries or package install steps;
- add bound-image metadata examples;
- add CI validation for image build and standards conformance.
