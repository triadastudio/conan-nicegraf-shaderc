from conans import ConanFile, CMake, tools
import os

class NicegrafShadercConan(ConanFile):
    name = "nicegraf-shaderc"
    short_paths = True  #windows MAX_PATH(260) limitation fix
    version = "0.6.1"
    license = "MIT"
    author = "<Bagrat Dabaghyan> <dbagrat@gmail.com>"
    url = "https://github.com/dBagrat/conan-nicegraf-shaderc.git"
    homepage = "https://github.com/nicebyte/nicegraf-shaderc"
    description = "nicegraf-shaderc is a command-line tool that transforms HLSL code into shaders for various graphics APIs"
    topics = ("shader compiler", "hlsl", "glsl", "metal")
    settings = "os_build", "arch_build", "arch", "compiler"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    no_copy_source = True

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/nicebyte/nicegraf-shaderc.git", "master", shallow=True)
        git.checkout("e5c98665b460e172f464fd073c9d7f3fb5deb7a5")

    def configure(self):
        del self.settings.compiler.runtime

    def build(self):
        cmake = CMake(self, build_type = "Release")
        cmake.configure()
        cmake.build(target = "nicegraf_shaderc")

    def package_id(self):
        self.info.include_build_settings()
        del self.info.settings.compiler
        del self.info.settings.arch

    def package(self):
        if self.settings.os_build == "Windows":
            self.copy("nicegraf_shaderc.exe", dst="bin", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
        else:
            self.copy("nicegraf_shaderc", dst="bin", keep_path=False)
            self.copy("*.dylib", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.bindirs = ['bin']
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))

