# ECHO controlled pilot

Actual browser/WebGL2 simulation, 24 primary runs + 1 repeat. See PROTOCOL.md and 实验结果报告.md. No consistent Q-learning advantage was demonstrated.

## Reproduce

Use Python 3: `python3 serve.py`, then open http://127.0.0.1:8101 in a WebGL2-capable browser and click Run benchmark. Results save to **rerun-results.json**, preserving the supplied original data. Same-device deterministic checks do not guarantee identical results on another GPU.

To regenerate the supplied analysis, install NumPy and Matplotlib into your Python environment and run `python3 analyze.py`. To analyze a new run, work in a copy of this directory and replace its raw-results.json with rerun-results.json first.

The protocol and source hashes were saved before execution. The engine derives from https://github.com/teknium1/genesis-engine (MIT; see source/LICENSE). This package includes the ECHO caretaker and benchmark wrapper. Initial-state hashes are matching checks, not cryptographic proofs. source-hashes.json contains SHA-256 source checksums.

The plot shows all 8 seeds; two expanding worlds dominate the arithmetic mean. Simulated mass is neither intelligence nor organism lifespan.
