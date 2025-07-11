from pathlib import Path

import moderngl as gl
import numpy as np
import cv2
from pyglm import glm
from OpenGL import GL

from texture import Texture
from cubemap import Cubemap
from image import Image
from mesh import MeshPart
from materials import Material, EquirectengularToCubemapMaterial, SingleCubemapMaterial
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

    captureSides = [
        GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X,
        GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
        GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
        GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
        GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
        GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
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
        environmentTexture = Texture.fromImage(image, gl.LINEAR, gl.LINEAR, False, False, dataType = "f2")

        equirectengularToCubemapShaderProgram = ShaderProgram("shaders/equirectengularToCubemapVertexShader.glsl", "shaders/equirectengularToCubemapFragmentShader.glsl")
        brdfLookupTableShaderProgram = ShaderProgram("shaders/passThroughVertexShader.glsl", "shaders/brdfLookupTableFragmentShader.glsl")
        self.cube = MeshPart.fromModel("res/models/cube.obj", EquirectengularToCubemapMaterial(equirectengularToCubemapShaderProgram, environmentTexture))
        self.quad = MeshPart.fromModel("res/models/quad.obj", Material(brdfLookupTableShaderProgram))

        self.environmentCubemap = self.captureShaderProgramOutputAsCubeMap(self.cube, 2048)

        diffuseIrradianceConvolutionShaderProgram = ShaderProgram("shaders/diffuseIrradianceConvolutionVertexShader.glsl", "shaders/diffuseIrradianceConvolutionFragmentShader.glsl")
        diffuseIrradianceConvolutionMaterial = SingleCubemapMaterial(diffuseIrradianceConvolutionShaderProgram, self.environmentCubemap)
        self.cube.setMaterial(diffuseIrradianceConvolutionMaterial)

        self.diffuseIrradienceCubemap = self.captureShaderProgramOutputAsCubeMap(self.cube, 64)

        specularPrefilteringShaderProgram = ShaderProgram("shaders/diffuseIrradianceConvolutionVertexShader.glsl", "shaders/specularPrefilteringFragmentShader.glsl")
        specularPrefilteringMaterial = SingleCubemapMaterial(specularPrefilteringShaderProgram, self.environmentCubemap)
        self.cube.setMaterial(specularPrefilteringMaterial)

        self.specularPrefilteredCubemap = self.captureSpecularPrefilterOutputAsMipmappedCubemap(self.cube, 256)

        self.brdfLookupTable = self.captureBrdfLookupTableAsTexture(self.quad, 512)

    def captureBrdfLookupTableAsTexture(self, quad: MeshPart, captureResolution):
        texture = Texture.createBlank(captureResolution, captureResolution, 2, dataType = "f2")

        renderBuffer = self.glContext.renderbuffer((captureResolution, captureResolution), 2, dtype = "f2")
        frameBuffer = self.glContext.framebuffer([renderBuffer])

        self.glContext.viewport = (0, 0, captureResolution, captureResolution)
        frameBuffer.use()
        self.glContext.clear()

        quad.render()
        data = frameBuffer.read(viewport = (0, 0, captureResolution, captureResolution), components = 2, dtype = "f2")
        texture.texture.write(data)

        self.glContext.screen.use()

        return texture

    def captureShaderProgramOutputAsCubeMap(self, meshPart: MeshPart, captureResolution):
        renderBuffer = self.glContext.renderbuffer((captureResolution, captureResolution), 3)
        frameBuffer = self.glContext.framebuffer(color_attachments = renderBuffer)

        cubemap = self.glContext.texture_cube((captureResolution, captureResolution), 3, dtype = "f2")

        meshPart.material.shaderProgram.setUniform("u_projectionTransform", EnvironmentMap.captureProjection)

        self.glContext.viewport = (0, 0, captureResolution, captureResolution)
        frameBuffer.use()

        for i in range(6):
            captureView = EnvironmentMap.captureViews[i]
            meshPart.material.shaderProgram.setUniform("u_viewTransform", captureView)

            self.glContext.clear()
            meshPart.render()

            cubemap.write(i, frameBuffer.read(viewport = (0, 0, captureResolution, captureResolution), components = 3, dtype = "f2"))

        self.glContext.screen.use()
        return cubemap
    
    def captureSpecularPrefilterOutputAsMipmappedCubemap(self, meshPart: MeshPart, highestCaptureResolution, numMipLevels = 5):
        frameBuffer = GL.glGenFramebuffers(1)
        renderBuffer = GL.glGenRenderbuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, frameBuffer)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, renderBuffer)
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT24, highestCaptureResolution, highestCaptureResolution)
        GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_RENDERBUFFER, renderBuffer)
        
        cubemap = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, cubemap)

        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_R, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

        GL.glTextureStorage2D(cubemap, numMipLevels, GL.GL_RGB16F, highestCaptureResolution, highestCaptureResolution)
        
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_BASE_LEVEL, 0)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAX_LEVEL, numMipLevels - 1)

        meshPart.material.shaderProgram.setUniform("u_projectionTransform", EnvironmentMap.captureProjection)

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, frameBuffer)
        for mipLevel in range(numMipLevels):
            mipSize = highestCaptureResolution >> mipLevel

            GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, renderBuffer)
            GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT24, mipSize, mipSize)
            GL.glViewport(0, 0, mipSize, mipSize)

            roughness = mipLevel / (numMipLevels - 1)
            meshPart.material.shaderProgram.setUniform("u_roughness", roughness)

            print(f"mip level: {mipLevel}, mip size: {mipSize}, roughness: {roughness}")
            
            for faceIndex in range(6):
                print("capturing face: ", faceIndex)
                captureView = EnvironmentMap.captureViews[faceIndex]
                captureSide = EnvironmentMap.captureSides[faceIndex]

                meshPart.material.shaderProgram.setUniform("u_viewTransform", captureView)
                
                GL.glFramebufferTexture2D(
                    GL.GL_FRAMEBUFFER,
                    GL.GL_COLOR_ATTACHMENT0,
                    captureSide,
                    cubemap,
                    mipLevel
                )
                GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0)

                GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

                meshPart.render()

        self.glContext.screen.use()

        return Cubemap(cubemap)

    def use(self, location = 0):
        self.environmentCubemap.use(location)