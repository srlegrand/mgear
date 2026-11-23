# mGear's plug-ins built for Aztek with its plug-in kit, from the same source as the Maya builds.
#
#   cmake -S aztek -B build-aztek -DAZTEK_DEVKIT=/path/to/Aztek/devkit -DCMAKE_BUILD_TYPE=Release
#   cmake --build build-aztek --config Release
#
#   mgear_solvers      ../src, unchanged
#   mGearWeightDriver  weightDriver/, the source/ folder of github.com/mgear-dev/mgear_weightDriver (3.6.3, 65a0133)
#   cvwrap             cvwrap/, the src/ folder of github.com/mgear-dev/cvwrap (882469a)
#   weightDriver       weightDriver-legacy/, Ingo Clemens' weightDriver 3.6.1 (github.com/mgear-dev/mgear_weightDriver at
#                      ca1fb04, before the rename), which rigs made with mGear 4 use
#
# The plug-ins are written to plug-ins/ in the build folder; package.py puts them in the module.

cmake_minimum_required(VERSION 3.16)
project(mgear_aztek CXX)

set(AZTEK_DEVKIT "" CACHE PATH "The devkit folder of Aztek's source")
if(NOT AZTEK_DEVKIT)
  message(FATAL_ERROR "Give -DAZTEK_DEVKIT=/path/to/Aztek/devkit")
endif()
# A relative folder is from the repository's root.
get_filename_component(AZTEK_DEVKIT "${AZTEK_DEVKIT}" ABSOLUTE BASE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/..")
find_package(AztekDevkit REQUIRED CONFIG PATHS "${AZTEK_DEVKIT}/cmake" NO_DEFAULT_PATH)

set(OUT "${CMAKE_BINARY_DIR}/plug-ins")

function(mgear_plugin name)
  aztek_add_plugin(${name} ${ARGN})
  set_target_properties(${name} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${OUT}"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG "${OUT}"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${OUT}"
    LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO "${OUT}")
endfunction()

file(GLOB SOLVERS "${CMAKE_CURRENT_SOURCE_DIR}/../src/*.cpp")
mgear_plugin(mgear_solvers SOURCES ${SOLVERS})

file(GLOB WEIGHT_DRIVER "${CMAKE_CURRENT_SOURCE_DIR}/weightDriver/*.cpp")
mgear_plugin(mGearWeightDriver SOURCES ${WEIGHT_DRIVER})

file(GLOB CVWRAP "${CMAKE_CURRENT_SOURCE_DIR}/cvwrap/*.cpp")
mgear_plugin(cvwrap SOURCES ${CVWRAP})

file(GLOB WEIGHT_DRIVER_LEGACY "${CMAKE_CURRENT_SOURCE_DIR}/weightDriver-legacy/*.cpp")
mgear_plugin(weightDriver SOURCES ${WEIGHT_DRIVER_LEGACY})
