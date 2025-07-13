import moderngl as gl
from pyglm import glm

from core import Core
from texture import Texture
from cubemap import Cubemap
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
    def __init__(self, shaderProgram: ShaderProgram, baseColorTexture: Texture, normalTexture: Texture,
                 metallicRoughnessTexture: Texture, ambientOcclusionTexture: Texture, emissiveTexture: Texture,
                 clearcoatWeight: float, clearcoatRoughness: float, clearcoatTint: glm.vec3,
                 diffuseIrradianceMap: gl.TextureCube, specularPrefilterMap: Cubemap, brdfLookuptable: Texture):
        super().__init__(shaderProgram)

        self.baseColorTexture = baseColorTexture
        self.normalTexture = normalTexture
        self.metallicRoughnessTexture = metallicRoughnessTexture
        self.ambientOcclusionTexture = ambientOcclusionTexture
        self.emissiveTexture = emissiveTexture
        self.clearcoatWeight = clearcoatWeight
        self.clearcoatRoughness = clearcoatRoughness
        self.clearcoatTint = clearcoatTint
        self.diffuseIrradianceMap = diffuseIrradianceMap
        self.specularPrefilterMap = specularPrefilterMap
        self.brdfLookuptable = brdfLookuptable
    
    def use(self):
        self.baseColorTexture.use(0)
        self.normalTexture.use(1)
        self.metallicRoughnessTexture.use(2)
        self.ambientOcclusionTexture.use(3)
        self.emissiveTexture.use(4)
        self.diffuseIrradianceMap.use(5)
        self.specularPrefilterMap.use(6)
        self.brdfLookuptable.use(7)

        self.shaderProgram.setUniform("u_clearcoatWeight", self.clearcoatWeight)
        self.shaderProgram.setUniform("u_clearcoatRoughness", self.clearcoatRoughness)
        #self.shaderProgram.setUniform("u_clearcoatTint", self.clearcoatTint)

class EquirectengularToCubemapMaterial(Material):
    def __init__(self, shaderProgram, environmentTexture: Texture):
        super().__init__(shaderProgram)

        self.environmentTexture = environmentTexture

    def use(self):
        self.environmentTexture.use(0)

class SingleCubemapMaterial(Material):
    def __init__(self, shaderProgram, cubemap: gl.TextureCube):
        super().__init__(shaderProgram)

        self.cubemap = cubemap
    
    def use(self):
        self.cubemap.use(0)