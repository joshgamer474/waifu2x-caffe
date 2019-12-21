from conans import ConanFile, CMake, tools
import os

class waifu2xcaffe(ConanFile):

    name = "waifu2x-caffe"
    version = "0.0.1"
    url = "https://github.com/lltcggie/waifu2x-caffe"
    description = "A screen sharing application"
    settings = {"os" : ["Windows"], 
                "arch": ["x86", "x86_64"],
                "compiler": ["Visual Studio"]}
    options = {"shared": [True, False],
               "cpu_only": [True, False]}
    generators = "cmake"
    requires = (
        "boost/1.71.0@conan/stable",
        "caffe/1.0.0@josh/lltcggie",
        "msgpack/3.2.0@bincrafters/stable",
        "rapidjson/1.1.0@bincrafters/stable",
        "stb/20190512@conan/stable",
        "tclap/1.2.1@josh/vcpkg",
        "spdlog/0.16.3@bincrafters/stable",
        )
    exports_sources = "bin/*", "common/*", "**/*.cpp", "**/*.h","CMakeLists.txt"
    default_options = "shared=False", "cpu_only=False"

    def configure(self):
        self.options["caffe"].shared = self.options.shared

    def imports(self):
        self.copy("*.dll", src="bin", dst="bin")
        self.copy("*", src="bin", dst="bin", root_package="waifu2x-caffe")

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        
        if self.options.cpu_only:
            cmake.definitions["CPU_ONLY"] = True
        cmake.definitions["CUDA_PATH"] = os.getenv('CUDA_PATH', "")
        cmake.configure()
        cmake.build()
        
    def package(self):
        self.copy("*", src="bin", dst="bin")
        self.copy("*.h", src="common", dst="include")
        self.copy("*_export.h", dst="include", keep_path=False)
        self.copy("*.lib", src="lib", dst="lib")
        self.copy("*.pdb", dst="lib", keep_path=False)