from conans import ConanFile, tools
import os

class NiceshadeTestConan(ConanFile):
    settings = "os_build", "arch_build"

    def imports(self):
        self.copy("niceshade*", dst="bin", src="bin")

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run("niceshade")
