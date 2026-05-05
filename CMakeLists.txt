cmake_minimum_required(VERSION 3.16)
project(executorch_baremetal_app C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(EXECUTORCH_ROOT ${CMAKE_SOURCE_DIR}/executorch)


if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")



option(EXECUTORCH_BUILD_CORTEX_M "Build for Cortex-M" ON)
option(EXECUTORCH_BUILD_EXTENSION_MODULE "Enable module extension" ON)
option(EXECUTORCH_BUILD_EXTENSION_TENSOR "Enable tensor extension" ON)
option(EXECUTORCH_BUILD_EXTENSION_DATA_LOADER "Enable data loader extension" ON)
option(EXECUTORCH_BUILD_EXTENSION_FLAT_TENSOR "Enable flat tensor extension" ON)
option(EXECUTORCH_BUILD_EXTENSION_NAMED_DATA_MAP "Enable named data map extension" ON)

set(EXECUTORCH_BUILD_PRESET_FILE
    ${EXECUTORCH_ROOT}/tools/cmake/preset/arm_baremetal.cmake
    CACHE FILEPATH "" FORCE
)

set(CMAKE_TOOLCHAIN_FILE
    ${EXECUTORCH_ROOT}/examples/arm/ethos-u-setup/arm-none-eabi-gcc.cmake
    CACHE FILEPATH "" FORCE
)

set(EXECUTORCH_BUILD_CORTEX_M ${EXECUTORCH_BUILD_CORTEX_M} CACHE BOOL "" FORCE)
set(EXECUTORCH_BUILD_EXTENSION_MODULE ${EXECUTORCH_BUILD_EXTENSION_MODULE} CACHE BOOL "" FORCE)
set(EXECUTORCH_BUILD_EXTENSION_TENSOR ${EXECUTORCH_BUILD_EXTENSION_TENSOR} CACHE BOOL "" FORCE)
set(EXECUTORCH_BUILD_EXTENSION_DATA_LOADER ${EXECUTORCH_BUILD_EXTENSION_DATA_LOADER} CACHE BOOL "" FORCE)
set(EXECUTORCH_BUILD_EXTENSION_FLAT_TENSOR ${EXECUTORCH_BUILD_EXTENSION_FLAT_TENSOR} CACHE BOOL "" FORCE)
set(EXECUTORCH_BUILD_EXTENSION_NAMED_DATA_MAP ${EXECUTORCH_BUILD_EXTENSION_NAMED_DATA_MAP} CACHE BOOL "" FORCE)

add_subdirectory(executorch)

add_executable(baremetal_app main.cpp)

target_link_libraries(baremetal_app PRIVATE executorch)

if(EXECUTORCH_BUILD_CORTEX_M)
    message(STATUS "Configuring Cortex-M build")

    target_compile_definitions(baremetal_app PRIVATE
        ET_BUILD_CORTEX_M
        ET_MINIMAL_RUNTIME
        ET_NO_EXCEPTIONS
    )

    target_compile_options(baremetal_app PRIVATE
        -Os
        -ffunction-sections
        -fdata-sections
    )

    target_link_options(baremetal_app PRIVATE
        -Wl,--gc-sections
    )
endif()
