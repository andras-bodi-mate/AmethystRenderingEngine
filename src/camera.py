from pyglm import glm

from debug import Debug

class Camera:
    def __init__(self, fov = 100):
        self.fov = fov
        self.position = glm.vec3(0.0, 0.0, 2)
        self.forward = glm.vec3(0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        aspectRatio = 1.777
        self.perspectiveTransform = glm.perspective(glm.radians(self.fov / aspectRatio), aspectRatio, 0.1, 1000.0)

    def getViewMatrix(self):
        elapsedTime = Debug.getElapsedTime()
        self.position = glm.vec3(glm.cos(elapsedTime * 0.2), 0, glm.sin(elapsedTime * 0.2)) * 2

        self.viewTransform = glm.lookAt(self.position, self.forward, self.up)
        return self.viewTransform