import riverline_core
import numpy as np
import torch

# 1. Load normalization constants
mean = np.load("state_mean.npy").tolist()
std = np.load("state_std.npy").tolist()

# 2. Initialize the C++ High-Speed Engine
engine = riverline_core.InferenceEngine("riverline_dqn_model.pt")
engine.set_normalization(mean, std)

# 3. Test a Real-Time Scenario
# Borrower: 45,000 INR debt, 120 days late, slightly angry (-0.1 sentiment)
debt, dpd, sentiment = 45000.0, 120.0, -0.1

print(f"\nIncoming Call Analysis...")
print(f"State: Debt=₹{debt}, DPD={dpd}, Sentiment={sentiment}")

# The Brain decides the action
action_idx = engine.predict(debt, dpd, sentiment)

action_map = {0: "0%", 1: "5%", 2: "10%", 3: "15%", 4: "20%", 5: "25%"}
print(f"Optimal Strategy calculated by C++ Engine: {action_map[action_idx]} discount.")