from pathlib import Path

import moderngl as gl
import numpy as np
from pyobjloader import load_model

from core import Core
from materials import Material

class MeshPart:
    @staticmethod
    def fromModel(modelPath: Path | str, material: Material):
        model = load_model(Core.getPath(modelPath))
        
        vertexData = np.array(model.vertex_points, dtype = np.float32).tobytes()
        indexData = np.array(model.point_indices, dtype = np.int32).tobytes()

        return MeshPart(vertexData, indexData = indexData, material = material)

    def __init__(self, vertexData: bytes, normalData: bytes = None, uvData: bytes = None, tangentData: bytes = None, indexData: bytes = None, material: Material = None):
        self.glContext = gl.get_context()

        assert indexData and material

        self.positionBuffer = self.glContext.buffer(vertexData)
        self.normalBuffer = self.glContext.buffer(normalData) if normalData else None
        self.uvBuffer = self.glContext.buffer(uvData) if uvData else None
        self.tangentBuffer = self.glContext.buffer(tangentData) if tangentData else None
        self.indexBuffer = self.glContext.buffer(indexData)

        self.material: Material
        self.vao: gl.VertexArray

        self.setMaterial(material)
    
    def setMaterial(self, newMaterial):
        self.material = newMaterial

        attributes = [
            (self.positionBuffer, "3f", "a_position"),
            *([(self.normalBuffer, "3f", "a_normal")] if self.normalBuffer else []),
            *([(self.uvBuffer, "2f", "a_uv")] if self.normalBuffer else []),
            *([(self.tangentBuffer, "3f", "a_tangent")] if self.tangentBuffer else [])
        ]

        self.vao = self.glContext.vertex_array(self.material.shaderProgram.shaderProgram, attributes, index_buffer = self.indexBuffer)

    def render(self):
        self.material.use()
        self.vao.render()

class Mesh:
    @staticmethod
    def fromModel(modelPath: Path | str, material: Material):
        return Mesh([MeshPart.fromModel(modelPath, material)])

    def __init__(self, parts: list[MeshPart]):
        self.glContext = gl.get_context()

        self.parts = parts

    def render(self):
        for part in self.parts:
            part.render()