cmake_minimum_required(VERSION 2.8.9)
project (waifu2x-caffe)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include(GenerateExportHeader)

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed
set(CMAKE_AUTOMOC ON)
# Create code from a list of Qt designer ui files
set(CMAKE_AUTOUIC ON)

add_compile_definitions(NO_STRICT)
add_compile_definitions(WIN32_LEAN_AND_MEAN)

set(COMMON
    common/cNet.cpp
    common/cNet.h
    common/stImage.cpp
    common/stImage.h
    common/waifu2x.cpp
    common/waifu2x.h)

set(WAIFU2X_CAFFE_CLI
    waifu2x-caffe/Source.cpp)

set(WAIFU2X_CAFFE_GUI
    waifu2x-caffe-gui/CControl.cpp
    waifu2x-caffe-gui/CControl.cpp
    waifu2x-caffe-gui/CControl.h
    waifu2x-caffe-gui/CDialog.cpp
    waifu2x-caffe-gui/CDialog.h
    waifu2x-caffe-gui/CDialogBase.cpp
    waifu2x-caffe-gui/CDialogBase.h
    waifu2x-caffe-gui/CWindow.h
    waifu2x-caffe-gui/CWindowBase.h
    waifu2x-caffe-gui/GUICommon.h
    waifu2x-caffe-gui/LangStringList.h
    waifu2x-caffe-gui/MainDialog.cpp
    waifu2x-caffe-gui/MainDialog.h
    waifu2x-caffe-gui/resource.h
    waifu2x-caffe-gui/Resource.rc
    waifu2x-caffe-gui/Source.cpp
    waifu2x-caffe-gui/Source.h
    waifu2x-caffe-gui/tstring.h)
    
set(WAIFU2X_CAFFE_DLL
    waifu2x-caffe-dll/Source.cpp)

file(TO_CMAKE_PATH ${CUDA_PATH} USE_CUDA_PATH)

message("********************************************")
message("CUDA_PATH: ${CUDA_PATH}")
message("********************************************")
message("USE_CUDA_PATH: ${USE_CUDA_PATH}")
message("********************************************")
message("CONAN_LIBS: ${CONAN_LIBS}")
message("********************************************")

include_directories(waifu2x-common
    include
    ${USE_CUDA_PATH}/include
    ${CONAN_INCLUDE_DIRS})

link_directories(${CONAN_LIB_DIRS}
    ${USE_CUDA_PATH}/lib/x64)

# Create common
add_library(waifu2x-common
    ${COMMON})
target_link_libraries(waifu2x-common
    ${CONAN_LIBS})
# Force debug symbols
target_compile_options(waifu2x-common PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/Zi>)

# Create waifu2x caffe library
add_library(waifu2x-caffe
    ${WAIFU2X_CAFFE_DLL})
target_link_libraries(waifu2x-caffe
    waifu2x-common
    ${CONAN_LIBS})

generate_export_header(waifu2x-caffe)

# Create waifu2x-caffe cli executable
add_executable(waifu2x-caffe-cli
    ${WAIFU2X_CAFFE_CLI})
target_link_libraries(waifu2x-caffe-cli
    waifu2x-common
    waifu2x-caffe
    ${CONAN_LIBS})
    #"-FORCE:multiple") # Force multiple definitions (!) to allow both protobuf and cuda-compiled-protobuf definitions


# Create GUI executable
#add_executable(waifu2x-caffe-gui
#    ${WAIFU2X_CAFFE_GUI})
#target_link_libraries(waifu2x-caffe-gui
#    waifu2x-common
#    waifu2x-caffe
#    ${CONAN_LIBS}
#    "-FORCE:multiple")

# Normalize CUDA_PATH
file(TO_CMAKE_PATH "$ENV{CUDA_PATH}" ENV_CUDA_PATH)

# Copy cudnn64_7.dll to bin
message("Copying ${ENV_CUDA_PATH}/bin/cudnn64_7.dll to ${CMAKE_BINARY_DIR}/bin/cudnn_data/cudnn64_7.dll")
add_custom_command(TARGET waifu2x-caffe POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy 
    ${ENV_CUDA_PATH}/bin/cudnn64_7.dll
    ${CMAKE_BINARY_DIR}/bin/cudnn_data/cudnn64_7.dll)

# Copy ./bin to bin
message("##################################")
message("Copying directory ${CMAKE_CURRENT_SOURCE_DIR}/bin to ${CMAKE_BINARY_DIR}/bin")
message("##################################")
add_custom_command(TARGET waifu2x-caffe POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${CMAKE_CURRENT_SOURCE_DIR}/bin
    ${CMAKE_BINARY_DIR}/bin)