# ECHO full review — build 2026.09.25-c

## Scope and corrections

Reviewed live application code, GPU equations, all four preset generators in both modes, controller/snapshot isolation, JSON input validation, storage loading, all wired control IDs, local links, desktop and 375px browser layout. This is an author-run engineering review, not an independent audit or proof of perpetual survival. Only this Chrome/WebGL environment was exercised; an actual phone and Safari were not tested.

- Preset switching previously silently advanced the seed and inherited environmental/paused state. Presets now start at seed 260924 with clean parameters, mutation 0 and learning off; switching produces a running fresh world unless reduced-motion preference pauses it.
- Random overlapping garden genomes and opposing pair configurations were unsuitable default starting points. Garden now has four matched separated bodies; Parallel pair has two matched diagonally separated bodies. Random field is explicitly named as a field, not a demonstrated origin of life.
- Evolution mode no longer starts with mutation automatically enabled. A chosen nonzero mutation or learned intervention can still end a run. No automatic reseeding or mass normalization is used.
- Completed runs retain a labeled last visible frame, ending step and measurements; Resume/Step/Add energy are disabled until a fresh or restored world is available. This is a recorded image, not living tissue. Rendering failures have a separate recovery path.
- Checkpoint Q-values and pending learning transitions are copied; random state is preserved. Previously an in-memory checkpoint could change with further learning. Disk and file imports share validation; unknown settings are discarded and malformed state rejected. A restore pauses before advancing.
- GPU energy: each neighbor transfer is capped to a quarter of the victim budget, exchanges use the same pre-metabolism state, and excess stored energy returns to the free pool instead of disappearing. Total-energy HUD now includes the free pool, so Add energy visibly adds 409.6 units.
- Simulation starts independently of storage retrieval. GPU errors are checked on rendering/readback, control exceptions become visible errors, and module URLs are versioned.
- PNG exports preserve proportions and label recorded end-state frames. Research Pilot 01 remains a separate unchanged historical simulator snapshot.

## Final default matrix

Same seed 260924, 128×128, dt 0.1, light 0.35, mutation 0, learning off; samples every 30 steps plus step 10000. false = fixed growth rules, true = evolving local genome enabled. All eight completed 10000 steps with visible tissue and finite GPU state.

| Case | Steps | Final mass |
|---|---:|---:|
| glider-false | 10000 | 75.8646 |
| glider-true | 10000 | 73.8373 |
| garden-false | 10000 | 303.2038 |
| garden-true | 10000 | 302.7322 |
| collide-false | 10000 | 151.0873 |
| collide-true | 10000 | 149.4541 |
| soup-false | 10000 | 3323.2001 |
| soup-true | 10000 | 3347.1944 |

## Boundary tests

24 additional runs: each of four worlds, both modes at light 0 and 1 (16), maximum mutation 0.015 (4), and seeded caretaker enabled (4); horizon 3000 or visible-tissue loss. All 16 zero-mutation light-boundary runs reached 3000. Three maximum-mutation and two caretaker runs ended early. Those are retained in stress.json, not counted as survival successes. No nonfinite measurements or GPU errors occurred. Largest absolute total-energy drift across the final 32 runs was 0.001812 units, from initial totals in the thousands.

The former Random field/seed 300519/evolution/mutation .003 failure at step 60 is preserved in before.json. Rejected intermediate layouts are retained in rejected-layout.json. Default seed/layout changes are explicit; results do not generalize to arbitrary imported worlds or edited parameters.

## Automated and UI checks

18 Node tests cover seed generation, caregiver feedback, checkpoint isolation/reproducible continuation, valid/invalid JSON round trips, old checkpoint compatibility, clean restart/preset changes, terminal pause and controls. Browser interaction checks cover pause/step/feed/save/restore, mode changes, mutation controls and narrow layout. All 27 original internal page references resolved; control IDs all matched. The versioned historical GitHub benchmark commit was verified accessible. No credential patterns were found in the published live files. This is not a penetration test.

## Reproduce

Serve this directory over HTTP, open defaults.html or stress.html, click Run, then download results. The preserved js directory contains the exact GPU stepping/preset/controller code used by these runs. Live UI and additional rendering error checks are in the project dist/js. hashes.json records this evidence. GPU results may differ on another device.
