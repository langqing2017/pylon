cmake_minimum_required(VERSION 2.8)
project(ctpinfo)

set(CMAKE_CXX_STANDARD 11)
set(platform x64)

set(CTP_DIR "${PROJECT_SOURCE_DIR}/../../libs/ctp/6.3.15_20190220_tradeapi64_se_windows")

include_directories(${PROJECT_SOURCE_DIR})
include_directories(${CTP_DIR})

link_directories(${CTP_DIR})

add_executable(ctpinfo main.cpp CtpTradeInterface.cpp)
target_link_libraries(ctpinfo thosttraderapi_se)
