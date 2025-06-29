import moderngl as gl

from core import Core

class Material:
    materials: list["Material"] = []

    @staticmethod
    def updateUniformForAllMaterials(uniform, value):
        for material in Material.materials:
            material.shaderProgram[uniform].write(value)

    def __init__(self, vertexShaderPath, fragmentShaderPath):
        self.glContext = gl.get_context()

        with open(Core.getPath(vertexShaderPath), 'r') as vertexShaderFile, open(Core.getPath(fragmentShaderPath), 'r') as fragmentShaderFile:
            self.shaderProgram = self.glContext.program(
                vertex_shader = vertexShaderFile.read(),
                fragment_shader = fragmentShaderFile.read()
            )

        Material.materials.append(self)