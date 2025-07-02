import moderngl as gl
from PIL import Image
from pyglm import glm

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
        return Texture(Image.new("RGB", (1, 1), glm.clamp(glm.ivec3(color * 255), 0, 255).to_tuple()), minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy)

    def __init__(self, image: Image.Image, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy = 16.0):
        self.glContext = gl.get_context()

        self.texture = self.glContext.texture(image.size, 3, image.tobytes())
        self.sampler = Sampler(self.texture, minificationFilter, magnificationFilter, doRepeatX, doRepeatY, anisotropy)

    def use(self, location = 0):
        self.sampler.use(location)