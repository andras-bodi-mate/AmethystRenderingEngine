import moderngl as gl

from core import Core
from texture import Texture
from shaderProgram import ShaderProgram

class Material:
    materials: list["Material"] = []

    @staticmethod
    def updateUniformForAllMaterials(uniform, value):
        for material in Material.materials:
            try:
                material.shaderProgram.setUniform(uniform, value)
            except KeyError:
                pass

    def __init__(self, shaderProgram: ShaderProgram):
        self.glContext = gl.get_context()

        self.shaderProgram = shaderProgram

        Material.materials.append(self)

    def use(self): pass

class PbrMaterial(Material):
    def __init__(self, shaderProgram: ShaderProgram, baseColorTexture: Texture, normalTexture: Texture, metallicRoughnessTexture: Texture):
        super().__init__(shaderProgram)

        self.baseColorTexture = baseColorTexture
        self.normalTexture = normalTexture
        self.metallicRoughnessTexture = metallicRoughnessTexture
    
    def use(self):
        self.baseColorTexture.use(0)
        self.normalTexture.use(1)
        self.metallicRoughnessTexture.use(2)

class EquirectengularToCubemapMaterial(Material):
    def __init__(self, shaderProgram, environmentTexture: Texture):
        super().__init__(shaderProgram)

        self.environmentTexture = environmentTexture

    def use(self):
        self.environmentTexture.use(0)