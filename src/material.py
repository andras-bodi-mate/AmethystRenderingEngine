from pathlib import Path

import moderngl as gl
from pygltflib import Material as gltfMaterial, GLTF2
from PIL import Image

from core import Core
from texture import Texture

class Material:
    materials: list["Material"] = []

    @staticmethod
    def updateUniformForAllMaterials(uniform, value):
        for material in Material.materials:
            material.shaderProgram[uniform].write(value)

    def __init__(self, vertexShaderPath: Path, fragmentShaderPath: Path, baseColorTexture: Texture):
        self.glContext = gl.get_context()

        with open(Core.getPath(vertexShaderPath), 'r') as vertexShaderFile, open(Core.getPath(fragmentShaderPath), 'r') as fragmentShaderFile:
            self.shaderProgram = self.glContext.program(
                vertex_shader = vertexShaderFile.read(),
                fragment_shader = fragmentShaderFile.read()
            )

        self.baseColorTexture = baseColorTexture

        Material.materials.append(self)

    def use(self):
        self.baseColorTexture.use()