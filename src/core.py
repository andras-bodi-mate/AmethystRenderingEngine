from os import path, sep

class Core:
    projectDir = path.abspath(path.join(path.dirname(__file__), ".."))

    @staticmethod
    def getPath(relativeProjectPath: str):
        return path.join(Core.projectDir, relativeProjectPath.replace('/', sep))