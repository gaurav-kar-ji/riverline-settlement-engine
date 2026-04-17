import riverline_core
import numpy as np

# 1. Load constants
mean = np.load("state_mean.npy").tolist()
std = np.load("state_std.npy").tolist()

# 2. Initialize
engine = riverline_core.InferenceEngine("riverline_dqn_model.pt")
engine.set_normalization(mean, std)

# SCENARIO A: Normal Borrower (Within training bounds)
# ~25k debt, 60 days late, neutral sentiment
print("--- SCENARIO A: Normal Operation ---")
idx, mode = engine.predict(25000.0, 60.0, 0.0)
print(f"Result: {mode} | Action Index: {idx}")

# SCENARIO B: The Black Swan (Out of Distribution)
# 1 Million INR debt (Huge outlier!), 500 days late, Extremely angry sentiment
# This should trigger the Safety Valve.
print("\n--- SCENARIO B: Black Swan Attack ---")
idx, mode = engine.predict(1000000.0, 500.0, -5.0)
print(f"Result: {mode} | Action Index: {idx}")

if mode == "SAFE_MODE_OOD":
    print("\nSUCCESS: The Safety Valve caught the outlier.")
else:
    print("\nFAILURE: The AI tried to guess. This is risky.")