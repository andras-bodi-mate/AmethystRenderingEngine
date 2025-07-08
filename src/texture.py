import moderngl as gl
from pyglm import glm
import numpy as np

from image import Image

class Sampler:
    def __init__(self, texture, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy = 16.0):
        self.glContext = gl.get_context()

        self.sampler = self.glContext.sampler(
            texture = texture
        )

    def use(self, location = 0):
        self.sampler.use(location)

class Texture:
    @staticmethod
    def fromColor(color: glm.vec3, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy = 16.0):
        imageData = np.array(((glm.clamp(glm.ivec3(color * 255), 0, 255).to_tuple(),),), dtype = np.uint8)
        return Texture(Image(imageData), minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy)

    def __init__(self, image: Image, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy = 16.0, dataType = "f1", internalFormat = None):
        self.glContext = gl.get_context()
        print(image.size, image.numComponents)
        self.texture = self.glContext.texture(image.size, image.numComponents, image.toBytes(), dtype = dataType, internal_format = internalFormat)
        self.sampler = Sampler(self.texture, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy)

    def use(self, location = 0):
        self.sampler.use(location)