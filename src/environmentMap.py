from pathlib import Path

import moderngl as gl
import numpy as np
from pyglm import glm

from texture import Texture
from image import Image
from mesh import Mesh, MeshPart
from materials import EquirectengularToCubemapMaterial
from shaderProgram import ShaderProgram

class EnvironmentMap:
    captureViews = [
        glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)),
        glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3(-1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)),
        glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  1.0,  0.0), glm.vec3(0.0,  0.0,  1.0)),
        glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0, -1.0,  0.0), glm.vec3(0.0,  0.0, -1.0)),
        glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  0.0,  1.0), glm.vec3(0.0, -1.0,  0.0)),
        glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  0.0, -1.0), glm.vec3(0.0, -1.0,  0.0))
    ]

    captureProjection = glm.perspective(glm.radians(90.0), 1.0, 0.1, 10.0)
    #captureProjection = glm.ortho(-0.5, 0.5, -0.5, 0.5, 0.1, 100.0)

    def __init__(self, imagePath: Path | str):
        self.glContext = gl.get_context()

        image = Image.open(imagePath, np.float16, True)
        print(image.size)
        newImageData = np.zeros((4096, 4096, 3), dtype = np.float16)
        newImageData[:2048, :, :] = image.data
        image.data = newImageData
        environmentTexture = Texture(image, gl.LINEAR, gl.LINEAR, False, False, dataType = "f2")

        equirectengularToCubemapShaderProgram = ShaderProgram("shaders/equirectengularToCubemapVertexShader.glsl", "shaders/equirectengularToCubemapFragmentShader.glsl")
        self.mesh = Mesh.fromModel("res/models/cube.obj", EquirectengularToCubemapMaterial(equirectengularToCubemapShaderProgram, environmentTexture))

        self.environmentCubemap = self.captureShaderProgramOutputAsCubeMap(equirectengularToCubemapShaderProgram, 2048)
        #self.diffuseIrradienceCubemap = self.captureShaderProgramOutputAsCubeMap()

    def captureShaderProgramOutputAsCubeMap(self, shaderProgram: ShaderProgram, captureResolution):
        renderBuffer = self.glContext.renderbuffer((captureResolution, captureResolution), 3)
        frameBuffer = self.glContext.framebuffer(color_attachments = renderBuffer)

        cubemap = self.glContext.texture_cube((captureResolution, captureResolution), 3, dtype = "f2")

        shaderProgram.setUniform("u_projectionTransform", EnvironmentMap.captureProjection)

        self.glContext.viewport = (0, 0, captureResolution, captureResolution)
        frameBuffer.use()

        for i in range(6):
            captureView = EnvironmentMap.captureViews[i]
            shaderProgram.setUniform("u_viewTransform", captureView)

            self.glContext.clear()
            self.mesh.render()

            cubemap.write(i, frameBuffer.read(components = 3, dtype = "f2"))

        self.glContext.screen.use()
        return cubemap

    def use(self, location = 0):
        self.environmentCubemap.use(location)