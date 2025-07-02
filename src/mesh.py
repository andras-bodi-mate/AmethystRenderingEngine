import moderngl as gl

from core import Core
from material import Material

class MeshPart:
    def __init__(self, vertexData: bytes, normalData: bytes, uvData: bytes, indexData: bytes, material: Material):
        self.glContext = gl.get_context()

        self.positionVbo = self.glContext.buffer(vertexData)
        self.normalVbo = self.glContext.buffer(normalData)
        self.uvVbo = self.glContext.buffer(uvData)
        self.ibo = self.glContext.buffer(indexData)

        self.material = material

        self.vao = self.glContext.vertex_array(self.material.shaderProgram, [
            (self.positionVbo, "3f", "in_position"),
            (self.normalVbo, "3f", "in_normal"),
            (self.uvVbo, "2f", "in_uv"),
        ], index_buffer = self.ibo)
    
    def render(self):
        self.material.use()
        self.vao.render()

class Mesh:
    def __init__(self, parts: list[MeshPart]):
        self.glContext = gl.get_context()

        self.parts = parts

    def render(self):
        for part in self.parts:
            part.render()