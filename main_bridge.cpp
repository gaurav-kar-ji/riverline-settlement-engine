#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "ai_core/inference_bridge.h"
namespace py = pybind11;
PYBIND11_MODULE(riverline_core, m) {
    py::class_<RiverlineInferenceEngine>(m, "InferenceEngine")
        .def(py::init<const std::string&>())
        .def("set_normalization", &RiverlineInferenceEngine::set_normalization)
        .def("predict", &RiverlineInferenceEngine::predict);
}