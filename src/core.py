from pathlib import Path, PurePosixPath

import glm

class Core:
    projectDir = Path(__file__).resolve().parent.parent

    @staticmethod
    def getPath(relativeProjectPath: str):
        return Core.projectDir / PurePosixPath(relativeProjectPath)
    
    @staticmethod
    def inverseLerp(start, end, value):
        return (value - start) / (end - start)
    
    @staticmethod
    def rotateY90(vec3: glm.vec3, direction = 1):
        return glm.vec3(-vec3.z * direction, vec3.y, vec3.x * direction)
    
    @staticmethod
    def convertMatrixIndex(column, row):
        return row, column