# nftables Templates

This directory is reserved for host packet policy templates used by the Socios immutable-node lane.

The initial `socios-default.nft` template did not land in this tranche because the connector safety filter blocked even placeholder variants.

## Expected contents

- `socios-default.nft` — reviewed baseline packet policy template for the immutable-node reference node.

## Constraints

1. The final nftables file should remain a standards template, not a site-specific production ruleset.
2. The final nftables file should be paired with explicit documentation and review expectations.
3. The final nftables file should align to `docs/HOST_CAPABILITY_MODEL.md` and `docs/IMMUTABLE_NODE_GUIDE.md`.
