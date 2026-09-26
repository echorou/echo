# ECHO stability review — 2026-09-25

This is a local Chrome/WebGL regression investigation, not evidence of intelligence or a token benefit. One glider configuration, seed 260924, 128 × 128, dt 0.1; samples every 30 steps. No reseeding, mass normalization or automatic recovery was applied within a run.

Before: the fixed original settings lost visible tissue at sampled step 690; the seeded Q-learning run at 390; setting mutation to zero alone at 1680. Fixed-genome and classic variants remained visible through 3000 steps. The caretaker PRNG seed was 12345; this reproduced the observed 390-step symptom but does not prove the user's complete click history.

After: four 10,000-step runs completed: fixed-genome default, corrected zero-mutation evolution, fixed-genome light 0, and fixed-genome light 1. Last scheduled sample is step 9990. Final sampled masses respectively: 75.5179, 76.0506, 74.4522, 76.6655. All peak masses were 1, all readback values finite, and GPU error checks passed. This does not establish indefinite survival, other worlds' survival, or cross-device reproducibility.

Corrections: newborn genetic jitter now scales with the mutation control (previously hard-coded even at zero). Default mode uses fixed growth rules and leaves learning off. Evolution is explicit and may collapse. Restart returns to the default glider; restored checkpoints pause. Wide canvases display one square world instead of repeating the same texture. Terminal decline is fed back to an enabled caretaker.

The original Pilot 01 data and source remain unchanged. These records are a separate regression audit. Before uses the simulator from commit d8f7692ca20a78674e426cff177b438309d13bf0. After uses the preserved simulator below with corrected birth jitter; subsequent viewport/error-handling edits do not change the step equations.

## Reproduce
Serve this directory over HTTP and open audit.html in a WebGL2 browser. Click Run stability audit. The browser runs the preserved after cases and offers a JSON download. The original local runner posted intermediate JSON to a local /results endpoint; the published runner downloads the same records instead. For before cases use before.json parameters and the earlier simulator commit; the caretaker random seed is 12345. Results can differ on other GPUs.
