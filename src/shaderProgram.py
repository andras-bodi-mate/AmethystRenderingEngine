from pathlib import Path

import moderngl as gl

from core import Core

class ShaderProgram:
    def __init__(self, vertexShaderPath: Path, fragmentShaderPath: Path):
        self.glContext = gl.get_context()

        with open(Core.getPath(vertexShaderPath), 'r') as vertexShaderFile, open(Core.getPath(fragmentShaderPath), 'r') as fragmentShaderFile:
            self.shaderProgram = self.glContext.program(
                vertex_shader = vertexShaderFile.read(),
                fragment_shader = fragmentShaderFile.read()
            )

    def setUniform(self, uniform, value):
        if isinstance(value, (float, int, bool, list, tuple)):
            self.shaderProgram[uniform] = value
        else:
            self.shaderProgram[uniform].write(value)