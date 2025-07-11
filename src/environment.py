from environmentMap import EnvironmentMap
from shaderProgram import ShaderProgram
from mesh import Mesh
from materials import Material

class Environment:
    def __init__(self, environmentMap: EnvironmentMap):
        self.environmentMap = environmentMap
        shaderProgram = ShaderProgram("shaders/skyBoxVertexShader.glsl", "shaders/skyBoxFragmentShader.glsl")

        self.mesh = Mesh.fromModel("res//models//backfaceCube.obj", Material(shaderProgram))

    def render(self):
        self.environmentMap.use()
        self.mesh.render()