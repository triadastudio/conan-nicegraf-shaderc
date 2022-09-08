from conans import ConanFile, CMake, tools
import os

class NiceshadeConan(ConanFile):
    name = "niceshade"
    version = "1.1.1"
    license = "MIT"
    url = "https://github.com/triadastudio/conan-niceshade.git"
    homepage = "https://github.com/nicebyte/niceshade"
    description = "niceshade is a library and a command-line tool that transforms HLSL code into shaders for various graphics APIs"
    topics = ("shader compiler", "hlsl", "glsl", "spirv", "metal")
    settings = "os_build", "arch_build", "arch", "compiler"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    no_copy_source = True

    @property
    def _source_commit(self):
        return "4daf21777314155031e16e031d6445cb5b981605"
    
    def source(self):
        tools.get(url="https://github.com/nicebyte/niceshade/archive/{}.zip"
                  .format(self._source_commit),
                  strip_root=True)

    def configure(self):
        del self.settings.compiler.runtime

    def build(self):
        cmake = CMake(self, build_type = "Release")
        cmake.configure()
        cmake.build(target = "niceshade")

    def package_id(self):
        self.info.include_build_settings()
        del self.info.settings.compiler
        del self.info.settings.arch

    def package(self):
        os = str(self.settings.os_build)
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
            }[os]

        except KeyError:
            self.output.error("Unsupported platform: {}".format(os))

        for pattern in [
            "niceshade{}".format(settings.get("ext", "")),
            "*.{}".format(settings["libext"])
        ]:
            self.copy(pattern, dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.bindirs = ["bin"]
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
