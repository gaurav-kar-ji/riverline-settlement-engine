import grpc
import engine_pb2
import engine_pb2_grpc

# The Business Translation Layer
OFFER_MAPPING = {
    0: "Demand Full Payment (0% Disc)",
    1: "Safe Baseline (Standard Procedure)",
    2: "3-Month Installment Plan",
    3: "6-Month Installment Plan",
    4: "Targeted 5% Settlement Discount",
    5: "Optimized 12% Settlement Discount"
}

def run_demo():
    channel = grpc.insecure_channel('localhost:50051')
    stub = engine_pb2_grpc.SettlementEngineStub(channel)

    # Scenarios described as "Business Cases"
    scenarios = [
        {
            "desc": "High Sentiment / Low Debt (Easy Recovery)",
            "data": {"debt": 15000.0, "dpd": 30, "sent": 0.8}
        },
        {
            "desc": "Anxious Borrower / Mid Debt (Negotiation Required)",
            "data": {"debt": 45000.0, "dpd": 95, "sent": -0.4}
        },
        {
            "desc": "Extreme Case (System Protection Check)",
            "data": {"debt": 950000.0, "dpd": 500, "sent": -0.9}
        }
    ]

    print("\n--- RIVERLINE AI SETTLEMENT ENGINE: LIVE DECISION LOG ---")
    
    for s in scenarios:
        print(f"\n[SCENARIO]: {s['desc']}")
        print(f"  Inputs -> Debt: ${s['data']['debt']}, DPD: {s['data']['dpd']}, Sentiment: {s['data']['sent']}")
        
        try:
            response = stub.GetOptimalDiscount(engine_pb2.StateRequest(
                debt_amount=s['data']['debt'],
                days_past_due=s['data']['dpd'],
                sentiment=s['data']['sent']
            ))
            
            decision = OFFER_MAPPING.get(response.action_index, "Unknown Action")
            
            # Highlight the "Mode" to show the Safety Shield vs AI Intelligence
            status_tag = f"[{response.mode}]"
            print(f"  ENGINE DECISION: {status_tag} -> {decision}")
            
        except Exception as e:
            print(f"  Connection Error: {e}")

if __name__ == "__main__":
    run_demo()