cmake_minimum_required(VERSION 3.15)
project(RiverlineAI)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# 1. Find Torch inside this folder ONLY
execute_process(COMMAND python3 -c "import torch; from pathlib import Path; print(Path(torch.__file__).parent / 'share' / 'cmake' / 'Torch')"
                OUTPUT_VARIABLE TORCH_CMAKE_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
set(CMAKE_PREFIX_PATH "${TORCH_CMAKE_PATH}")
find_package(Torch REQUIRED PATHS "${TORCH_CMAKE_PATH}" NO_DEFAULT_PATH)

# 2. Build the AI brain as a SHARED library (Binary Encapsulation)
add_library(ai_engine_core SHARED inference_bridge.cpp)

# 3. THE FIREWALL: Link Torch as PRIVATE.
# This ensures Torch headers are NEVER exported to the server.
target_link_libraries(ai_engine_core PRIVATE "${TORCH_LIBRARIES}")
target_include_directories(ai_engine_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# ABI Sync
execute_process(COMMAND python3 -c "import torch; print(int(torch._C._GLIBCXX_USE_CXX11_ABI))"
                OUTPUT_VARIABLE PYTHON_ABI OUTPUT_STRIP_TRAILING_WHITESPACE)
target_compile_definitions(ai_engine_core PRIVATE _GLIBCXX_USE_CXX11_ABI=${PYTHON_ABI})