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
    def fromColor(color: glm.vec3, numComponents = 3, minificationFilter = gl.LINEAR, magnificationFilter = gl.LINEAR, doRepeatX = False, doRepeatY = False, anisotropy = 16.0, dataType = "f1", internalFormat = None):
        if dataType == "f1":
            if isinstance(color, (list, tuple)):
                match len(color):
                    case 1:
                        unclampedColor = glm.ivec1(glm.vec1(color) * 255)
                    
                    case 2:
                        unclampedColor = glm.ivec2(glm.vec2(color) * 255)

                    case 3:
                        unclampedColor = glm.ivec3(glm.vec3(color) * 255)

                    case 4:
                        unclampedColor = glm.ivec4(glm.vec4(color) * 255)

            else:
                if isinstance(color, (glm.vec1, float, int)):
                    unclampedColor = glm.ivec1(color * 255)

                elif isinstance(color, glm.vec2):
                    unclampedColor = glm.ivec2(color * 255)

                elif isinstance(color, glm.vec3):
                    unclampedColor = glm.ivec3(color * 255)

                elif isinstance(color, glm.vec4):
                    unclampedColor = glm.ivec4(color * 255)

            pixel = glm.clamp(unclampedColor, 0, 255)

        elif isinstance(color, (float, int)):
            pixel = glm.vec1(color)

        else:
            pixel = color

        imageData = np.array(((pixel.to_tuple(),),), dtype = np.uint8 if dataType == "f1" else np.float16)
        return Texture(1, 1, numComponents, imageData, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy, dataType, internalFormat)
    
    @staticmethod
    def fromImage(image: Image, minificationFilter = gl.LINEAR, magnificationFilter = gl.LINEAR, doRepeatX = False, doRepeatY = False, anisotropy = 16.0, dataType = "f1", internalFormat = None, generateMipMaps = False):
        return Texture(image.size[0], image.size[1], image.numComponents, image.data, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy, dataType, internalFormat, generateMipMaps)

    @staticmethod
    def createBlank(width: int, height: int, numComponents = 3, minificationFilter = gl.LINEAR, magnificationFilter = gl.LINEAR, doRepeatX = False, doRepeatY = False, anisotropy = 16.0, dataType = "f1", internalFormat = None):
        return Texture(width, height, numComponents, None, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy, dataType, internalFormat)

    def __init__(self, width: int, height: int, numComponents = 3, data: bytes = None, minificationFilter = gl.LINEAR, magnificationFilter = gl.LINEAR, doRepeatX = False, doRepeatY = False, anisotropy = 16.0, dataType = "f1", internalFormat = None, generateMipMaps = False):
        self.glContext = gl.get_context()
        self.texture = self.glContext.texture((width, height), numComponents, data, dtype = dataType, internal_format = internalFormat)
        self.sampler = Sampler(self.texture, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy)

        if generateMipMaps:
            self.texture.build_mipmaps()

    def use(self, location = 0):
        self.sampler.use(location)
        self.texture.use(location)