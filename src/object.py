from abc import ABC

import moderngl as gl
from pyglm import glm

from mesh import Mesh
from material import Material

class Object:
    def __init__(self, mesh: Mesh):
        self.glContext = gl.get_context()

        self.mesh = mesh

class SingleObject(Object):
    def __init__(self, mesh):
        super().__init__(mesh)

    def render(self):
        self.mesh.render()

class InstancedObject(Object):
    pass