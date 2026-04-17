#include <iostream>
#include <memory>
#include <grpcpp/grpcpp.h>
#include "engine.pb.h"
#include "engine.grpc.pb.h"
#include "inference_bridge.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::Status;
using riverline::SettlementEngine;

class SettlementEngineImpl final : public SettlementEngine::Service {
    std::unique_ptr<RiverlineInferenceEngine> engine;
public:
    SettlementEngineImpl() {
        engine = std::make_unique<RiverlineInferenceEngine>("riverline_dqn_model.pt");
        engine->set_normalization({25000.0f, 90.0f, 0.0f}, {15000.0f, 45.0f, 0.5f});
    }

    Status GetOptimalDiscount(grpc::ServerContext* context, const riverline::StateRequest* req,
                              riverline::ActionResponse* res) override {
        auto [idx, mode] = engine->predict(req->debt_amount(), req->days_past_due(), req->sentiment());
        res->set_action_index(idx);
        res->set_mode(mode);
        return Status::OK;
    }
};

int main() {
    SettlementEngineImpl service;
    ServerBuilder builder;
    builder.AddListeningPort("0.0.0.0:50051", grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server live on 50051" << std::endl;
    server->Wait();
    return 0;
}