from conan import ConanFile
from conan.tools import build, files

class NiceshadeTestConan(ConanFile):
    settings = "arch", "build_type", "compiler", "os"

    def imports(self):
        files.copy(self, "niceshade*", dst="bin", src="bin")

    @property
    def _settings_build(self):
        return getattr(self, "settings_build", self.settings)

    def build_requirements(self):
        self.build_requires(self.tested_reference_str)

    def test(self):
        if build.can_run(self):
            with files.chdir(self, self.build_folder):
                self.run("niceshade")
