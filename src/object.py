import moderngl as gl

from mesh import Mesh
from material import Material

class Object:
    def __init__(self, mesh: Mesh, material: Material):
        self.glContext = gl.get_context()

        self.mesh = mesh
        self.material = material

        self.vao: gl.VertexArray

class SingleObject(Object):
    def __init__(self, mesh, material):
        super().__init__(mesh, material)

        self.vao = self.glContext.vertex_array(self.material.shaderProgram, self.mesh.vbo, "in_position", index_buffer = self.mesh.ibo)

    def draw(self):
        self.vao.render()

class InstancedObject(Object):
    pass