# Case Study: Riverline High-Performance Settlement Engine
## The Strategy Gap
Riverline currently treats debt recovery as a language and workflow automation problem. This creates a significant revenue gap. Debt negotiation is actually a dynamic pricing problem that requires mathematical precision. Relying on LLMs to guess settlement discounts during a live call leads to uncalibrated offers and lost yield. Furthermore, Python based inference introduces latency that breaks the natural rhythm of a voice agent.
## Engineered Solution
This engine separates the conversation from the math. While the LLM handles the dialogue, this C++ core dictates the exact financial terms in real time. It treats every borrower interaction like a dynamic order book. The system calculates the mathematically optimal settlement discount or EMI structure during the call without adding any perceptible delay.

## Financial Impact
Moving from static discount policies to a dynamic reinforcement learning engine increases the expected value of recovery. The engine focuses on the probability of payment multiplied by the settlement amount. This transition from basic automation to algorithmic pricing directly increases recovery rates and profit margins.
## System Design
* `C++ Inference Core` : Built with LibTorch to bypass the Python global interpreter lock. This ensures sub microsecond execution for seamless voice integration.
* `Safety Shield` : Includes out of distribution detection. If borrower data falls outside known bounds, the system reverts to a conservative fallback mode to protect the business.
* `gRPC Integration`: Uses a high throughput network protocol. This allows any existing backend to connect to the pricing engine through a clean contract.

## Repository Guide
* `ai_core` : Contains the isolated C++ vault for the model logic
* `engine.proto` : Defines the gRPC service contract
* `server.cpp` : The standalone high performance server implementation
* `verify_service.py` : A script to validate the network loop and safety triggers

## Build Instructions
### 1. Compile the engine: 
```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
```
### 2. Launch the Service:
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/ai_core
./riverline_server
```
### 3. Run Validation:
```bash
python3 verify_service.py
```
## Action Policy Mapping
This table defines the business logic executed by the C++ engine based on the model's output index.

| Action Index | Settlement Offer Type | Business Impact |
| :--- | :--- | :--- |
| **0** | No Discount (Demand Full) | High Margin / High Default Risk |
| **1** | **Standard Fallback** | **Safety Baseline (Safe Mode)** |
| **2** | 3-Month EMI Plan | Cash Flow Smoothing |
| **3** | 6-Month EMI Plan | High Retention / Slow Recovery |
| **4** | 5% One-time Settlement | Targeted Incentive |
| **5** | **12% Aggressive Settlement** | **Maximized Yield for High-Risk Borrower** |
### Developed by : Dweepayan Kar
