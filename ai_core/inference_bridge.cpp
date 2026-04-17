#include "inference_bridge.h"
#include <torch/script.h>

class RiverlineInferenceEngine::Impl {
public:
    torch::jit::script::Module module;
    std::vector<float> mean;
    std::vector<float> std_dev;
    bool loaded = false;

    Impl(const std::string& path) {
        try {
            module = torch::jit::load(path);
            module.eval();
            loaded = true;
        } catch (...) {}
    }
};

RiverlineInferenceEngine::RiverlineInferenceEngine(const std::string& path) 
    : pimpl(new Impl(path)) {}

RiverlineInferenceEngine::~RiverlineInferenceEngine() { delete pimpl; }

void RiverlineInferenceEngine::set_normalization(std::vector<float> m, std::vector<float> s) {
    pimpl->mean = m;
    pimpl->std_dev = s;
}

std::pair<int, std::string> RiverlineInferenceEngine::predict(double debt, double dpd, double sentiment) {
    if (!pimpl->loaded) return {0, "ERROR"};

    float n_debt = (float(debt) - pimpl->mean[0]) / (pimpl->std_dev[0] + 1e-8);
    float n_dpd = (float(dpd) - pimpl->mean[1]) / (pimpl->std_dev[1] + 1e-8);
    float n_sent = (float(sentiment) - pimpl->mean[2]) / (pimpl->std_dev[2] + 1e-8);

    if (std::abs(n_debt) > 3.5 || std::abs(n_dpd) > 3.5 || std::abs(n_sent) > 3.5)
        return {1, "SAFE_MODE_OOD"};

    torch::Tensor input = torch::tensor({{n_debt, n_dpd, n_sent}});
    at::Tensor output = pimpl->module.forward({input}).toTensor();
    return {output.argmax(1).item<int>(), "AI_OPTIMIZED"};
}