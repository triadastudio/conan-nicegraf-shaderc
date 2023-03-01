from conan import ConanFile
from conan.tools import cmake, files

import os

class NiceshadeConan(ConanFile):
    name = "niceshade"
    version = "1.1.2"
    license = "MIT"
    url = "https://github.com/triadastudio/conan-niceshade.git"
    homepage = "https://github.com/nicebyte/niceshade"
    description = "niceshade is a library and a command-line tool that transforms HLSL code into shaders for various graphics APIs"
    topics = ("shader compiler", "hlsl", "glsl", "spirv", "metal")
    settings = "os", "arch", "compiler", "build_type"
    package_type = "application"
    generators = "CMakeToolchain"
    no_copy_source = True

    @property
    def _source_commit(self):
        return "2b6feea686beb05dffd3ba2e2705896bfc6e9bd2"

    def configure(self):
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.runtime")

    def layout(self):
        cmake.cmake_layout(self)

    def source(self):
        files.get(self,
                  url="https://github.com/nicebyte/niceshade/archive/{}.zip".format(self._source_commit),
                  strip_root=True)

    def build(self):
        cm = cmake.CMake(self)
        cm.configure()
        cm.build(target = "niceshade")

    def package_id(self):
        del self.info.settings.arch
        del self.info.settings.compiler
        del self.info.settings.build_type

    def package(self):
        os_str = str(self.settings.os)
        try:
            settings = {
                "Windows": {
                    "ext": ".exe",
                    "libext": "dll"
                },
                "Macos": {
                    "libext": "dylib"
                },
                "Linux": {
                    "libext": "so"
                }
            }[os_str]

        except KeyError:
            self.output.error("Unsupported platform: {}".format(os_str))

        for pattern in [
            "niceshade{}".format(settings.get("ext", "")),
            "*.{}".format(settings["libext"])
        ]:
            print(pattern)
            files.copy(self,
                       pattern,
                       src=self.source_folder,
                       dst=os.path.join(self.package_folder, "bin"),
                       keep_path=False)

    def package_info(self):
        self.cpp_info.bindirs = ["bin"]
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
