cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
project(fun_math VERSION 0.1.0 LANGUAGES CXX)

add_executable(fun_math fun_math_lib.cpp)
add_library(dot_prod dot_prod.cpp)
target_link_libraries(fun_math PUBLIC dot_prod)
target_include_directories(fun_math PUBLIC "${PROJECT_SOURCE_DIR}")