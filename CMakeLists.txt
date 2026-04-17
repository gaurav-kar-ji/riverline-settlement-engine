cmake_minimum_required(VERSION 3.15)
project(RiverlineSystem)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_IGNORE_PATH "/mnt/c;/mnt/d;/mnt/e")

# 1. System Dependencies (NO TORCH MENTIONED HERE)
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# 2. Proto Generation
set(proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/engine.pb.cc")
set(proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/engine.pb.h")
set(grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/engine.grpc.pb.cc")
set(grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/engine.grpc.pb.h")

add_custom_command(
      OUTPUT "${proto_srcs}" "${proto_hdrs}" "${grpc_srcs}" "${grpc_hdrs}"
      COMMAND /usr/bin/protoc --cpp_out "${CMAKE_CURRENT_BINARY_DIR}" 
                     --grpc_out "${CMAKE_CURRENT_BINARY_DIR}" 
                     --plugin=protoc-gen-grpc=/usr/bin/grpc_cpp_plugin
                     -I "${CMAKE_CURRENT_SOURCE_DIR}" 
                     "${CMAKE_CURRENT_SOURCE_DIR}/engine.proto"
      DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/engine.proto")

# 3. Add AI Core
add_subdirectory(ai_core)

# 4. Build Standalone Server
add_executable(riverline_server server.cpp ${proto_srcs} ${grpc_srcs})

# THE 1% MANEUVER: Explicitly force system paths to the top
target_include_directories(riverline_server BEFORE PRIVATE "/usr/include")
target_include_directories(riverline_server PRIVATE "${CMAKE_CURRENT_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")

# Link to the .so binary. Since it's a SHARED library, headers don't leak.
target_link_libraries(riverline_server PRIVATE ai_engine_core gRPC::grpc++ protobuf::libprotobuf)

# 5. Python Bridge
include(FetchContent)
FetchContent_Declare(pybind11 GIT_REPOSITORY https://github.com/pybind/pybind11.git GIT_TAG v2.10.4)
FetchContent_MakeAvailable(pybind11)

file(WRITE ${CMAKE_CURRENT_SOURCE_DIR}/main_bridge.cpp 
    "#include <pybind11/pybind11.h>\n#include <pybind11/stl.h>\n#include \"ai_core/inference_bridge.h\"\n"
    "namespace py = pybind11;\nPYBIND11_MODULE(riverline_core, m) {\n"
    "    py::class_<RiverlineInferenceEngine>(m, \"InferenceEngine\")\n"
    "        .def(py::init<const std::string&>())\n"
    "        .def(\"set_normalization\", &RiverlineInferenceEngine::set_normalization)\n"
    "        .def(\"predict\", &RiverlineInferenceEngine::predict);\n}")

pybind11_add_module(riverline_core main_bridge.cpp)
target_link_libraries(riverline_core PRIVATE ai_engine_core)