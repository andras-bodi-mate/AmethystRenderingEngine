import moderngl as gl
from pyobjloader import load_model

from core import Core

class Mesh:
    def __init__(self, path):
        self.glContext = gl.get_context()

        self.model = load_model(Core.getPath(path))
        self.model.format = "3f"
        self.model.attribs = ["in_position"]

        self.vbo = self.glContext.buffer(self.model.vertex_points)
        self.ibo = self.glContext.buffer(self.model.point_indices)