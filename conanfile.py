from conans import ConanFile, CMake, tools
import os

class waifu2xcaffe(ConanFile):

    name = "waifu2x-caffe"
    version = "0.0.1"
    url = "https://github.com/lltcggie/waifu2x-caffe"
    description = "A screen sharing application"
    settings = {"os" : ["Windows"], 
                "arch": ["x86", "x86_64"],
                "build_type": ["Debug", "Release", "RelWithDebInfo"],
                "compiler": ["Visual Studio"]}
    options = {"shared": [True, False],
               "cpu_only": [True, False]}
    generators = "cmake"
    requires = (
        "boost/1.68.0@conan/stable",
        "caffe/1.0.0@josh/lltcggie",
        "msgpack/3.2.0@bincrafters/stable",
        "rapidjson/1.1.0@bincrafters/stable",
        "stb/20190512@conan/stable",
        "tclap/1.2.2@josh/testing",
        "spdlog/0.16.3@bincrafters/stable",
        )
    exports_sources = "bin/**", "common/*", "**/*.cpp", "**/*.h","CMakeLists.txt"
    default_options = "shared=True", "cpu_only=False"

    def configure(self):
        self.options["boost"].shared = True
        self.options["caffe"].shared = self.options.shared

    def imports(self):
        self.copy("*.dll", dst="bin", keep_path=False)

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        
        if self.options.cpu_only:
            cmake.definitions["CPU_ONLY"] = True
        cmake.definitions["CUDA_PATH"] = os.getenv('CUDA_PATH', "")
        cmake.configure()
        cmake.build()
        
    def package(self):
        self.copy("*", src="bin", dst="bin", excludes="**/cudnn64_7.dll")
        self.copy("*.h", src="common", dst="include")
        self.copy("*_export.h", dst="include", keep_path=False)
        self.copy("*.lib", src="lib", dst="lib")
        self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["waifu2x-common-d", "waifu2x-caffe-d"]
        else:
           self.cpp_info.libs = ["waifu2x-common", "waifu2x-caffe"]