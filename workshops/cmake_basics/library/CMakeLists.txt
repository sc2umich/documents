cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
SET(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
project(fun_math VERSION 0.1.0 LANGUAGES CXX)

add_executable(fun_math fun_math_lib.cpp)
target_include_directories(fun_math PUBLIC "${PROJECT_SOURCE_DIR}")
target_link_libraries(fun_math "${CMAKE_SOURCE_DIR}/dot_prod.a")