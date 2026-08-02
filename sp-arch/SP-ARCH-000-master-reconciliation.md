# SP-ARCH-000 — Master Reconciliation & Unified Backlog

**Status:** Proposed (intake + reconciliation, not implementation)
**Date:** 2026-08-02
**Owner:** M. Heller
**Absorbs / reconciles:** SP-ARCH-001 (invariants, four planes), SP-ARCH-002 (inject reconciliation), SP-ARCH-003 (fibered twin integration), SP-ARCH-004 (Sociosphere = star machine), the two inject-batch reconciliations, the 13-artifact Estate Integration Map, the MeshRush Omni-Crystal spec, and the Orchestration/DAG/Materialization spec (`sp-orchestrator`).
**Epistemic status:** This document is `Speculative` synthesis. Every repo-existence claim in §2 is `Measured` (verified via `gh` on 2026-08-02). Nothing here is `Proved`.

---

## 0. Scope discipline (read first)

This is a **capture + validate + sequence** pass over a large spec corpus. It is **not** an implementation, and the corpus is weeks of build across ~15 repos. Per standing practice (spec-corpus intake), the attached files are **registered, not bulk-read** (§6). The value delivered here is:

1. the finding that the whole corpus is **one loop instantiated many ways** (§1),
2. **consistency corrections** against the live estate — the corpus contains several factual errors (§2),
3. the **cross-cutting decisions** that must be settled before any build (§3),
4. a **unified WO backlog** with real repo homes and a critical path (§4–5).

---

## 1. The unification — the actual finding

Every artifact in the corpus is a re-parameterisation of a single loop, already named SCOPE-D in SP-ARCH-002:

```
declared M → predict x̂ → observe z → residual r = z − h(x̂)
           → epistemicLevel (posterior variance) → GATE (policy-fabric)
           → actuate (capability token) | halt+escalate → ProofArtifact → HellGraph → M
```

The estate has **already built the algebra this loop runs on** — `sp-orchestrator` (WO-01..05, all merged). The ADRs are that algebra, instantiated at increasing structure:

| Layer | Artifact | What it instantiates | Home |
|---|---|---|---|
| **Algebra / execution** | `sp-orchestrator` (BUILT) | EpistemicLevel lattice + `meet`, manifest-as-task-key input, join provenance, attestation | `sp-orchestrator` |
| **The loop** | SP-ARCH-002 / SCOPE-D | declared→observed→residual→gate; 14 injects = estimators/types/schedules | `SCOPE-D` |
| **The loop, indexed** | SP-ARCH-003 (fibration) | loop over extent lattice `B` × lifecycle `T`; residual = unit of `f_! ⊣ f*`; `meet` forced by functoriality (FIB-4) | `gaia-world-model` + `hellgraph` |
| **The loop, surfaced** | SP-ARCH-004 (star machine) | workspace = materialised star; mount=`f*`, publish=`f_!`; mount table = capability surface | `prophet-workspace` / `sociosphere` |
| **The loop, as compile** | MeshRush Omni-Crystal | observe→diffuse→crystallize; compile certificate = attestation; artifact = durable cell | `meshrush` |
| **The conductor** | (new) | declares manifests, gates entrances not notes; = M. Heller as conductor agent | new role, not a service |

**Consequence:** these are not competing designs to choose between. They are one architecture at five altitudes. `meet_all([]) = Speculative` appears independently in sp-orchestrator (house rule), SP-ARCH-002 (§6), and SP-ARCH-003 (FIB-4, as a theorem). That triple-derivation is the signal the unification is real.

The residual operator is the load-bearing seam and it now has **named implementations** from the inject batches:
- continuous low-dim state → **Kalman filter** (batch-2 Img 11)
- discrete/process state → **conformance alignment** (batch-1 Img 5, van der Aalst)
- graph-propagated knowledge → **GAT + temporal decay** (batch-2 Img 2/4)
- scheduling/allocation → **MAPPACS** multi-agent PPO (batch-2 Img 9)
- policy representation → **symbolic policy under multi-env genetic fitness** (batch-2 Img 8), *preferred over* PSO-Mamdani

These are estimator-agnostic at the seam: `f_!` only ever moves *residuals and epistemic levels*, so fibers may declare different estimators and still compose (§3 D-D).

---

## 2. Consistency validation against the live estate (CORRECTIONS)

All repo states verified via `gh` on 2026-08-02.

| Corpus claim | Verified reality | Action |
|---|---|---|
| Integration Map §2.4: **ProCybernetica** is repo-less/new | **EXISTS** `SocioProphet/ProCybernetica` (canonical home of Semantic Coordinate Algebra) | Strike from "net-new." Bind Darwin-IPC (F4/img4) forensic authority onto it. |
| §2.4: **Sherlock/Holmes** not in repo list | **EXIST** `SocioProphet/sherlock-search`, `SocioProphet/holmes` | Strike from "net-new." |
| Artifact 7: **Alexandrian Academy** "no confirmed repo" | **EXISTS** `SocioProphet/alexandrian-academy` | Strike from "net-new." Learning loop lands here, not a new repo. |
| §2.3: "**Triune RPC**" (img11) = "**TriRPC**" (img12), collapse to one | **Michael 2026-08-02: correct — `TriTRPC` ≡ `TriuneRPC` ≡ TriRPC, one ternary-native RPC transport.** (Supersedes an earlier estate note that wrongly said "≠ TriuneRPC".) | **Collapse to one.** Decision D-B RESOLVED. |
| **GAIA** = world model / types (ADRs) | Overloaded: `gaia-world-model` (ADR sense) **and** weather-domain `prophet-domain-gaia-ontology` / `-curation-vault` | ADR GAIA ≡ `gaia-world-model`. Decision D-C on the weather collision. |
| SP-ARCH-002 assigns WO-5/6/9 to **TritFabric** | `tritfabric` is **active** (pushed 2026-07-31), but a prior estate note marked it "mlops-suite absorbed / DEAD" | Reconcile: live or revived? Verify ownership before assigning WOs. |
| §2.1: **four independent ledgers** (Reserve-Heller, Moirai, Aegis Vault, MCP-A2A audit) | Estate already has `prophet-core-ledger` + `model-governance-ledger` | Decision D-A: typed views over one event-sourced ledger. |
| §2.2: **memory-mesh** is the single memory substrate | **EXISTS** `SocioProphet/memory-mesh`; correct | Confirmed. Fold Michael/Contextual-Memory + QES trace-cache into it. |
| §2.4: **HyperSwarm mesh** node-discovery repo-less | No repo owns gossip/rendezvous/placement | **Genuinely net-new.** |
| Artifact 13 / §2.4: **federated big-data plane** (Spark/Beam/Drill/Iceberg) | Nothing in estate does federated query planning | **Genuinely net-new.** Build-vs-buy (D-F). |

**Net:** of the corpus's four "repo-less" domains, **two are false** (already built) and **two are real** (HyperSwarm mesh, federated big-data plane).

---

## 3. Cross-cutting decisions — settle before any build

| ID | Decision | Recommendation | Gates |
|---|---|---|---|
| **D-A** | Ledger unification | One event-sourced, append-only ledger (`prophet-core-ledger`) with **typed views**: economic (Reserve-Heller), governance changeset (Moirai), evidence (Aegis Vault), session audit (MCP-A2A). Four sources of truth violates "no invisible authority." | all settlement/audit WOs |
| **D-B** | Transport identity | **RESOLVED (Michael 2026-08-02): `TriTRPC` ≡ `TriuneRPC` — same transport**, also folds "Triune RPC" (img11) / "TriRPC" (img12). One transport impl (`SocioProphet/TriTRPC`, ternary-native RPC) shared by `regis-entity-graph` + sovereign cloud-shell. | img11/img12 WOs |
| **D-C** | GAIA naming | ADR GAIA = `gaia-world-model` (site/types). Weather GAIA stays `prophet-domain-gaia-*`. Document the split so no third GAIA is minted. | SP-ARCH-003 |
| **D-D** | Estimator registry | Per-fiber estimator declaration behind one residual interface: Kalman \| conformance-alignment \| GAT-decay \| MAPPACS \| symbolic-policy. Residual/epi are estimator-agnostic; `f_!` transports only those. | WO-1, WO-15 |
| **D-E** | Superconscious (D8) | Ships **only** if the sedenion zero-divisor identifiability monitor beats a variance-threshold baseline on the synthetic non-identifiability ROC suite. Until then, out of all external material. Highest narrative risk. | WO-11, WO-17 |
| **D-F** | Build-vs-buy | NetBox (Apache-2.0 ✓), Spark/Beam/Drill/Iceberg (Apache-2.0 ✓) all license-clean but **wrap, don't merge** (generalise the OpenConnector decision). HyperSwarm mesh + federated plane = new repos. | img6, img13 WOs |
| **D-G** | MeshRush fold-in | DECIDED (this session): fold the Omni-Crystal scientific engine into the existing `meshrush` repo, filling its acknowledged stub slots; run it on `sp-orchestrator`; extend governance to `agent-machine` + `prophet-mesh` via the conductor. | MR-WO-00.. |
| **D-H** | nauty/Traces license | nauty/Traces is Apache-2.0 since 2.6 (MIT/Apache-only constraint OK) — **verify the exact version** before wiring the symmetry cascade. | MR-WO-04 |

---

## 4. Unified WO backlog (single numbering, real homes)

Legend: ✅ done · 🔨 build · 🔀 subsumed/re-scope · ⛔ blocked on decision.

### 4.0 Foundation — `sp-orchestrator` (✅ DONE)
| WO | Title | Home | State |
|---|---|---|---|
| ORCH-01..05 | Cell/EpistemicLevel/meet · registry · task-key · exec+grant · join+meet | `sp-orchestrator` | ✅ PR#1–6 merged; accept#9 lineage 0.25:1 |
| ORCH-06 | (next) IVM + expansion points + adjudication cascade | `sp-orchestrator` | 🔨 owed |

### 4.1 The loop — SP-ARCH-002 (SCOPE-D)
| WO | Title | Home | Dep / note |
|---|---|---|---|
| A2-1 | Conformance-checking residual estimator → computed `epistemicLevel` | `policy-fabric`/`hellgraph` | **first**; Kalman first-pass (batch-2), alignment for discrete |
| A2-2 | BMG-1 invariant + Layer-1/Layer-2 gate | `agent-registry` | **first**; unblocks all actuation |
| A2-3 | Ontogenesis gated stage ladder + demotion | `ontogenesis` | 🔀 see A3 (fibration re-scopes) |
| A2-4 | Six-edge interaction ontology | `hellgraph` | 🔀 subsumed by A3-WO-12 |
| A2-5 | MissionScore six-axis emission | `tritfabric` | ⛔ D-A? no; verify tritfabric (D-2 reconcile) |
| A2-6 | Deferred defuzzification (or symbolic policy) | `tritfabric` | prefer symbolic-policy (batch-2 img8) |
| A2-7 | ControlParameter registry + envelopes | `exodus` | — |
| A2-8 | AgentLoadRecord + ACWR drift | `agentplane` | ACWR bands = priors, recalibrate |
| A2-9 | Replay buffer as ProofArtifact evidence | `tritfabric` | needs ray_runner placeholder-metric fix |
| A2-10 | VFL tenancy + ProofArtifact degradation | `semantic-serdes` | ⛔ legal (data-min review) |
| A2-11 | Superconscious embedding φ + falsification harness | `superconscious`/`Noetica` | ⛔ D-E |

### 4.2 The loop, indexed — SP-ARCH-003 (fibration)  *(WO-12..14 subsume A2-1 & A2-4)*
| WO | Title | Home | Dep |
|---|---|---|---|
| A3-12 | Extent lattice `B` + coverage | `gaia-world-model`/`hellgraph` | ⛔ PPG disambiguation (§0.2 of A3) |
| A3-13 | `f*`/`f_!` transport + ProofArtifact inclusion record | `hellgraph` | A3-12 |
| A3-14 | Residual as unit `η` (unifies A2-1) | `policy-fabric` | A3-13 |
| A3-15 | Per-fiber estimator registry | (D-D) | A3-13 |
| A3-16 | Descent checker (overlap agreement + obstruction) | `hellgraph` | A3-13 |
| A3-17 | Superconscious identifiability verdict | `superconscious` | ⛔ D-E; A3-16 |
| A3-18 | Cohort sieves + k-anon floor | `policy-fabric` | ⛔ legal |
| A3-19 | Lifecycle fibration + footprint monoid + incl-excl | `ontogenesis`/`exodus` | — |
| A3-20 | Decay-law calibration (replaces unset θ/W) | `ontogenesis` | A3-19 |
| A3-21 | Symbolic policy evolution (supersedes Mamdani) | `tritfabric` | A2-6 |

### 4.3 The loop, surfaced — SP-ARCH-004 (star machine / Sociosphere)
| WO | Title | Home | Dep |
|---|---|---|---|
| A4-22 | Mount table = capability surface (+diff) | `prophet-workspace` | ⛔ §12 repo-divergence check first |
| A4-23 | mount = `f*` with authority check in `B` | `prophet-workspace` | A4-22, A3-13 |
| A4-24 | publish = `f_!` (gate + incl-excl + Heller settle) | `prophet-workspace` | A4-23 |
| A4-25 | live residual (continuous η) | `prophet-workspace` | A4-23/24 |
| A4-26 | descent verdict per mount + degraded read-only | `prophet-workspace` | A3-16 |
| A4-27 | obstruction UX (localise disagreement in place) | `prophet-workspace` | A4-26 |
| A4-28 | external workspace issuance (STAR-1..3) | `sociosphere` | A4-23 |
| A4-29 | star cache + in-session decay | `prophet-workspace` | A3-19 |
| A4-30 | **SP-File Naming as reference impl** (thin e2e) | `prophet-workspace` | A4-22/23; **best first proof** |

### 4.4 The loop, as compile — MeshRush (D-G)
| WO | Title | Home | Dep |
|---|---|---|---|
| MR-00 | Reconciliation + charter: fold engine into `meshrush`, unify framing (observation-first default), deprecate `Basic*` stubs, MIT, CI (tests+lint+gate/check), depend on `sp-orchestrator` | `meshrush` | — |
| MR-01 | `core/graph_build` + `omni/reduction`: W,D,L,P + diffusion coords | `meshrush` | MR-00 |
| MR-02 | `crystal/dynamics`: support-density `c` + crystallinity `φ` + band term + MBO | `meshrush` | MR-01 |
| MR-03 | `omni/probes`: impulse / spectral / seed-persistence / symmetry | `meshrush` | MR-01 |
| MR-04 | `crystal/symmetry`: cascade (prepartition→ε-role→nauty→egonet→probe-equivariance) + defect functionals | `meshrush` | ⛔ D-H (nauty license); MR-03 |
| MR-05 | compression: VQ codebook + IB relevance | `meshrush` | MR-02 |
| MR-06 | `crystal/compile` + 6-gate certificate; **certificate→attestation, artifact→durable cell, epi mapping** (the sp-orchestrator seam) | `meshrush` | MR-02/04/05 |
| MR-07 | experiment matrix (structural/dynamical/observation-first; encode 129-vs-141 correction) | `meshrush` | MR-06 |
| MR-08 | governance seam: meshrush loop as sp-orchestrator DAG + ExpansionPoints; govern `agent-machine` receipts + `prophet-mesh` choir; conductor manifest | `meshrush` + `agent-machine` + `prophet-mesh` | MR-06, ORCH-06 |

### 4.5b Ecosystem Simulation Substrate — the market-intelligence cartridge (6th loop instantiation)
Intake 2026-08-02. Two WOs: v1 "Ecosystem Reporting Substrate" (descriptive fact store) **superseded by** v2 "Ecosystem Simulation Substrate" (causal, interventional). This is the **Investor-Insights / market-view cartridge**; homes = `economic-prophet` + `regis-entity-graph` + `hellgraph`. It is the same canonical loop at the causal layer:
- **identifiability gate** (refuse point estimate for unidentified estimand → bounds + blocking structure) = the `epistemicLevel` refusal / `meet_all([])=Speculative` rule for causal inference.
- **two-layer SCM(governance)/solver(execution)** — "Layer B never runs on an estimand Layer A has not cleared" = **BMG-1** (Layer2 "may we claim this" / Layer1 "what is the value").
- content-addressed reproducible scenario = ORCH `task_key`/`dag_id`+attestation; read-set invalidation = ORCH §5.3 IVM; SIMULATED-scoring via natural experiments = adjudication/retroactive cascade.
- **Wave-1 SCM identification engine = `causal_abduction.py`** — the pipeline the 13-artifact map flagged as blocking the whole economics flywheel. This program IS that fix.

| WO | Title | Home | Dep |
|---|---|---|---|
| ECO-1 | SCM layer + identification engine + estimand registry + **refusal path** (`causal_abduction.py` exposed route) | `economic-prophet` | ⛔ D-I; unblocks economics flywheel |
| ECO-2 | Parameter facts with propagating uncertainty (edge transfer_fn/lead-time distributions; scenario output = distribution, never scalar) | `economic-prophet`/`hellgraph` | ECO-1 |
| ECO-3 | Ecosystem graph node/edge model + traversal + per-hop coverage report | `regis-entity-graph`/`hellgraph` | 🔀 reuse A3 fibration coverage |
| ECO-4 | Solvers: discrete-event supply + choice model + L0/L1 reaction; scenario artifact + deterministic replay | `economic-prophet` | ECO-2 |
| ECO-5 | Realtime: precomputed sensitivity/influence, read-set tracking, delta invalidation, staleness decay | `economic-prophet` | 🔀 reuse ORCH IVM; ECO-4 |
| ECO-6 | Strategic L2/L3 reaction + natural-experiment retrospective scoring | `economic-prophet` | ECO-4; needs event-history density |
| ECO-7 | Multi-tenant contamination control (k-anon + **differencing-attack budget**, output-side screening) | `policy-fabric`/`semantic-serdes` | ⛔ legal; 🔀 shares A3-18 k-anon |
| ECO-8 | Filing cadence + renderers (benchmark + market-view, recommendation gate, audience-scoped license enforcement) | `economic-prophet` | ECO-4 |

### 4.5 Genuinely net-new (D-F)
| WO | Title | Home | Note |
|---|---|---|---|
| NEW-1 | HyperSwarm mesh: node discovery / gossip / rendezvous / placement | new repo | from img12 sovereign cloud-shell |
| NEW-2 | Federated big-data control plane (wrap Spark/Beam/Drill/Iceberg) | new repo | build-vs-buy, wrap-don't-merge |
| NEW-3 | Fog-node runtime (img12) | `agent-machine`? or new | verify vs agent-machine cluster substrate |

---

## 5. Critical path

```
sp-orchestrator (✅) 
   └─► A2-1/A3-14 residual estimator + A2-2 BMG-1 gate      [the two cheap unblockers]
          └─► A3-12→13 extent lattice + f*/f_! transport     [subsumes A2-4]
                 └─► A4-22→23→30 star-machine thin slice (SP-File Naming e2e)
                        └─► everything else parallel (≤11 subagents)
MeshRush: MR-00 can start immediately in parallel (independent repo); MR-08 joins at ORCH-06.
```

**Recommended first build (thin vertical slice that proves the whole architecture):**
1. **A2-1 + A2-2** — conformance/Kalman residual → computed `epistemicLevel`, and the BMG-1 Layer-1/2 gate. Both cheap, both unblock everything.
2. **A4-30** — SP-File Naming publishing through the Sociosphere gate: smallest real agent that exercises mount(`f*`)→work→publish(`f_!`)→ProofArtifact end to end.
3. **MR-00** — MeshRush reconciliation PR (parallel, independent).

---

## 6. Attached-files intake register (registered, not bulk-read)

| File | Size | First read | Maps to | Note |
|---|---|---|---|---|
| `Six-Deck_Deconstruction_Correlation_Resynthesis.docx` | 20K | needs `docx` skill | likely the 6-deck reconciliation upstream of the 13-artifact map | deep-read next |
| `multiverseal-twin-spec.pdf` | 291K | needs `pdf` read | **SP-ARCH-003 fibered twins** (the "multiverseal" = multi-extent fibration) | deep-read next; probable primary source for A3 |
| `resilient-loader-and-diagnostics-spec.md` | 23K | markdown, cheap | `sourceos-boot` / `agent-machine` launch | resilient boot/loader + diagnostics |
| `rld-reference-implementation.zip` | 63K | Rust workspace | same | **carries a Lean proof** `rld-proof/LaunchCompleteness.lean` → a `Proved`-tier artifact; crates: `types/harness/rdr/solver/store/launch` |

The RLD bundle is notable: it is the only corpus item with a **machine-checkable proof** (`LaunchCompleteness.lean`) — i.e. genuinely `Proved`-tier, the top of the epistemic lattice. Worth prioritising its reconciliation because it demonstrates the `proved` level the whole lattice is designed around.

---

## 7. Homes & next action

- **This document** wants a durable home: propose `SP-ARCH-000` in `sourceos-spec` or `prophet-platform-standards` (canonical spec surfaces), or a new `sp-arch` repo if the ADR series deserves its own home.
- **Governance:** any commit via isolated worktree, rebase+push upstream, MIT/Apache, gate/check required, Copilot review before merge (note: only `prophet-platform` currently has Copilot wiring).
- **Owed decisions:** D-A (ledger), D-B (transport identity), D-C (GAIA), plus PPG disambiguation (blocks A3-12) and the tritfabric live/dead reconciliation.
```