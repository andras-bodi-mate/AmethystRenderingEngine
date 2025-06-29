from functools import reduce

import moderngl as gl
from pyglm import glm

from mesh import Mesh
from material import Material
from transform import Transform

class Object:
    def __init__(self, mesh: Mesh, transform: Transform, debugName: str | None = None):
        self.glContext = gl.get_context()

        self.mesh = mesh
        self.transform = transform
        self.children: list["Object"] = []
        self.debugName = debugName

class SingleObject(Object):
    def __init__(self, mesh: Mesh, transform: Transform, debugName: str | None = None):
        super().__init__(mesh, transform, debugName)

    def render(self, ancestorTransforms: list[Transform] | None = None):
        if self.mesh:
            finalObjectTransform = self.transform.transformation if not ancestorTransforms else reduce(lambda a, b: a * b, ancestorTransforms + [self.transform.transformation])

            for part in self.mesh.parts:
                part.material.shaderProgram["objectTransform"].write(finalObjectTransform)

            self.mesh.render()

        if self.children:
            for child in self.children:
                child.render((ancestorTransforms or []) + [self.transform.transformation])

class InstancedObject(Object):
    pass