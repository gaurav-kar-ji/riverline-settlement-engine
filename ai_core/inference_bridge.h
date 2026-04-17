#ifndef INFERENCE_BRIDGE_H
#define INFERENCE_BRIDGE_H

#include <string>
#include <vector>
#include <utility>

class RiverlineInferenceEngine {
public:
    RiverlineInferenceEngine(const std::string& model_path);
    ~RiverlineInferenceEngine();
    void set_normalization(std::vector<float> m, std::vector<float> s);
    std::pair<int, std::string> predict(double debt, double dpd, double sentiment);

private:
    class Impl; 
    Impl* pimpl;
};
#endif