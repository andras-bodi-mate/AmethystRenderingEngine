from functools import reduce

import moderngl as gl
from pyglm import glm

from mesh import Mesh
from transform import Transform

class Object:
    def __init__(self, mesh: Mesh, transform: Transform, name: str | None = None):
        self.glContext = gl.get_context()

        self.mesh = mesh
        self.transform = transform
        self.children: list["Object"] = []
        self.name = name

class SingleObject(Object):
    def __init__(self, mesh: Mesh, transform: Transform, debugName: str | None = None):
        super().__init__(mesh, transform, debugName)

    def render(self, parentTransform: Transform = None):
        if self.mesh:
            finalObjectTransform = parentTransform.transformation * self.transform.transformation if parentTransform else self.transform.transformation

            for part in self.mesh.parts:
                part.material.shaderProgram.setUniform("u_objectTransform", finalObjectTransform)

            self.mesh.render()

        if self.children:
            for child in self.children:
                child.render(self.transform)

class InstancedObject(Object):
    pass