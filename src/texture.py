import moderngl as gl
from PIL import Image

from core import Core

class Texture:
    def __init__(self, imagePath):
        self.glContext = gl.get_context()

        with Image.open(Core.getPath(imagePath)) as image:
            self.texture = self.glContext.texture(image.size, image.format)