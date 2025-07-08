from pathlib import Path

import moderngl as gl
import numpy as np
from pyobjloader import load_model

from core import Core
from materials import Material

class MeshPart:
    def __init__(self, vertexData: bytes, normalData: bytes = None, uvData: bytes = None, indexData: bytes = None, material: Material = None):
        self.glContext = gl.get_context()

        assert indexData and material

        self.positionVbo = self.glContext.buffer(vertexData)
        self.normalVbo = self.glContext.buffer(normalData) if normalData else None
        self.uvVbo = self.glContext.buffer(uvData) if uvData else None
        self.ibo = self.glContext.buffer(indexData)

        self.material = material

        attributes = [
            (self.positionVbo, "3f", "a_position"),
            *([(self.normalVbo, "3f", "a_normal")] if self.normalVbo else []),
            *([(self.uvVbo, "2f", "a_uv")] if self.normalVbo else []),
        ]

        self.vao = self.glContext.vertex_array(self.material.shaderProgram.shaderProgram, attributes, index_buffer = self.ibo)
    
    def render(self):
        self.material.use()
        self.vao.render()

class Mesh:
    @staticmethod
    def fromModel(modelPath: Path | str, material: Material):
        model = load_model(Core.getPath(modelPath))
        
        vertexData = np.array(model.vertex_points, dtype = np.float32).tobytes()
        indexData = np.array(model.point_indices, dtype = np.int32).tobytes()

        return Mesh([MeshPart(vertexData, indexData = indexData, material = material)])

    def __init__(self, parts: list[MeshPart]):
        self.glContext = gl.get_context()

        self.parts = parts

    def render(self):
        for part in self.parts:
            part.render()