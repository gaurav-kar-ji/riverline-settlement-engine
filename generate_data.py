import riverline_core
import pandas as pd
import random
import time

NUM_EPISODES = 500000
POSSIBLE_ACTIONS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25] # 0% to 25% discounts

print(f"Generating {NUM_EPISODES} synthetic negotiation trajectories...")
start_time = time.time()

data = []

for episode in range(NUM_EPISODES):
    debt = random.uniform(1000.0, 50000.0)
    dpd = random.randint(30, 180)
    init_sentiment = random.uniform(-0.2, 0.2)
    
    env = riverline_core.DebtSimulator(debt, dpd, init_sentiment)
    state = env.reset()
    is_done = False
    
    while not is_done:
        action = random.choice(POSSIBLE_ACTIONS)
        next_state, reward, is_done = env.step(action)
        
        data.append({
            "state_debt": state[0],
            "state_dpd": state[1],
            "state_sentiment": state[2],
            "action_discount": action,
            "reward": reward,
            "next_state_debt": next_state[0],
            "next_state_dpd": next_state[1],
            "next_state_sentiment": next_state[2],
            "is_done": is_done
        })
        
        state = next_state

df = pd.DataFrame(data)
df.to_parquet("riverline_training_data.parquet", engine="pyarrow")

elapsed = time.time() - start_time
print(f"Generated {len(df)} transitions in {elapsed:.2f} seconds.")
print("Saved to 'riverline_training_data.parquet'.")