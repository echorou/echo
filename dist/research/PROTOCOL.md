# ECHO matched-world pilot — protocol fixed before execution

Date: 2026-09-25. Scope: an exploratory comparison of the current online caretaker, not a claim of biology, intelligence, token utility, or investment value.

## Design

- World: upstream `garden`, 128 × 128 cells, radius 13. Seeds 101–108. Each seed is one matched block. The generator creates three initial Orbium stamps with randomized locations, orientations, genome mu, and aggression; overlap can change initial total mass.
- Three policies: FIXED uses caretaker action 0 (light .35, mutation .002) throughout; RANDOM selects uniformly among the four existing caretaker actions every 180 steps; Q_LEARNING uses the unchanged Caretaker algorithm with seeded exploration, beginning at step 180. All groups start at the same action-0 settings, not the app's mutation .003 default.
- Use identical initial float arrays within each block; record an initial-state hash. Rotate run order by seed to avoid putting one policy consistently first. Same browser/GPU, serial execution.
- All other engine parameters held fixed: dt .1; genome/metabolism/eat enabled; mass conservation disabled; predPayoff .35; no added energy, curiosity, manual pokes, save/restore, or external intervention.
- 1,800 steps per run; full telemetry every 30 steps including step 0. One fresh untrained Q table per Q-learning run. Action choice at 180, 360, …, 1620; no unused decision at endpoint 1800. This yields only eight completed Q updates: a short cold-start test, not a test of a pretrained controller.
- Intervention PRNG: LCG with initial uint32(seed + 9001). No uncontrolled Math.random in controller. SAME RNG seed for random/Q does not imply same sampled choices because their draw consumption differs.
- 24 primary runs (8 matched worlds × 3 policies), plus one FIXED seed-101 exact-repeat check, excluded from aggregate results. Do not stop runs at decline, select good seeds afterwards, tune on outcomes, or add trials based on results.

## Outcomes fixed in advance

Primary: time-averaged mass ratio = trapezoidal integral of [total cell mass / initial total cell mass] over the 1,800-step horizon, divided by 1,800. This is a biomass proxy; dense static patterns can score highly. It is not a count of living organisms, ecosystem complexity, or intelligence.

Secondary: final mass ratio; time-averaged stored creature energy ratio to initial stored creature energy; occupied-cell fraction (mass > .1); average per-cell absolute mass change between 30-step samples (pattern activity); first detected sustained decline.

Sustained decline: mass below 10% of initial mass at 10 consecutive 30-step observations (a discrete observation rule). Report detection step, not a biological death time. If not detected before 1,800, mark right-censored at the horizon; never label 1,800 as actual lifespan. Runs continue even after a decline event.

## Analysis

Show all eight paired outcomes, medians and means, and descriptive paired differences Q−FIXED and Q−RANDOM. Include exact paired sign-flip randomization p-values for the primary metric as exploratory only (no confirmatory efficacy claim); n=8 is small and multiple comparisons are not a preregistered confirmatory trial. No claim of significance, generalization, or causality outside this configured simulator. Confidence intervals, if included, must be identified as exploratory and not imply biological efficacy.

Record browser/GPU characteristics, code SHA-256, parameter set, PRNG, run order, action history, every telemetry observation, failures, elapsed times and repeat-check agreement. A GPU error or non-finite state invalidates the run; report it rather than silently replacing the trial.
