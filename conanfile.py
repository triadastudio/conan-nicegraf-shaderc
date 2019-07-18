from conans import ConanFile, CMake, tools

class NicegrafShadercConan(ConanFile):
    name = "nicegraf-shaderc"
    short_paths = True  #windows MAX_PATH(260) limitation fix
    version = "0.1"
    license = "MIT"
    author = "<Bagrat Dabaghyan> <dbagrat@gmail.com>"
    url = "https://github.com/dBagrat/conan-nicegraf-shaderc.git"
    homepage = "https://github.com/nicebyte/nicegraf-shaderc"
    description = "nicegraf-shaderc is a command-line tool that transforms HLSL code into shaders for various graphics APIs"
    topics = ("shader compiler", "hlsl", "glsl", "metal")
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    no_copy_source = True

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/nicebyte/nicegraf-shaderc.git", "master")
        git.checkout("fcf1965e98a9f841fa60297f0a1a18e13e9e88c0")

    def configure(self):
        del self.settings.compiler.runtime

    def build(self):
        cmake = CMake(self, build_type="Release")
        cmake.configure()
        cmake.build(target = "nicegraf_shaderc")

    def package(self):
        self.copy("nicegraf_shaderc.exe", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.bindirs = ['bin']

