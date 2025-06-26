import moderngl as gl

from core import Core

class Material:
    def __init__(self, vertexShaderPath, fragmentShaderPath):
        self.glContext = gl.get_context()

        with open(Core.getPath(vertexShaderPath), 'r') as vertexShaderFile, open(Core.getPath(fragmentShaderPath), 'r') as fragmentShaderFile:
            self.shaderProgram = self.glContext.program(
                vertex_shader = vertexShaderFile.read(),
                fragment_shader = fragmentShaderFile.read()
            )