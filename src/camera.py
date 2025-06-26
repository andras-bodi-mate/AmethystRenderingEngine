from pyglm import glm

from debug import Debug

class Camera:
    def __init__(self, fov = 100):
        self.fov = fov
        self.position = glm.vec3(0.0, 0.0, 2)
        self.forward = glm.vec3(0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.perspectiveTransform: glm.mat4x4
        self.updateMatrices(1.0)

    def updateMatrices(self, aspectRatio):
        elapsedTime = Debug.getElapsedTime()
        self.position = glm.vec3(glm.cos(elapsedTime * 0.5), 0, glm.sin(elapsedTime * 0.5)) * 2

        self.perspectiveTransform = glm.perspective(glm.radians(self.fov), aspectRatio, 0.1, 1000.0)

        self.viewTransform = glm.lookAt(self.position, self.forward, self.up)