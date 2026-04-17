import grpc
import engine_pb2
import engine_pb2_grpc

def run_test():
    # Connect to the C++ Server
    channel = grpc.insecure_channel('localhost:50051')
    stub = engine_pb2_grpc.SettlementEngineStub(channel)

    # Scenarios to test model inference and the Safety Shield
    scenarios = [
        {"name": "Standard Case", "debt": 25000.0, "dpd": 60, "sent": 0.1},
        {"name": "Out-of-Distribution", "debt": 900000.0, "dpd": 500, "sent": -0.9}
    ]

    print(f"{'Scenario':<20} | {'Mode':<15} | {'Action Index'}")
    print("-" * 50)

    for s in scenarios:
        try:
            # Call the C++ binary over the network
            response = stub.GetOptimalDiscount(engine_pb2.StateRequest(
                debt_amount=s["debt"],
                days_past_due=s["dpd"],
                sentiment=s["sent"]
            ))
            print(f"{s['name']:<20} | {response.mode:<15} | {response.action_index}")
        except grpc.RpcError as e:
            print(f"Network Error: {e.details()}")

if __name__ == "__main__":
    run_test()