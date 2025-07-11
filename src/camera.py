from pyglm import glm

from core import Core
from debug import Debug

class Camera:
    def __init__(self, fov = 80, cameraPath = None, cameraPathScale = 1.0):
        self.fov = fov
        self.position = glm.vec3(0.0, 1, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.projectionTransform: glm.mat4x4

        if cameraPath:
            self.cameraPath: list[glm.vec3] = []

            with open(Core.getPath(cameraPath), "r") as cameraPathMeshFile:
                for line in cameraPathMeshFile.readlines():
                    if line[0] == 'v':
                        self.cameraPath.append(glm.vec3(*map(float, line[2:].split())) * cameraPathScale)
        else:
            self.cameraPath = None
        
        self.updateMatrices(1.0)

    def getCameraPathNormalAtIndex(self, index):
        numSegments = len(self.cameraPath)

        p1 = self.cameraPath[(index - 25) % numSegments]
        p2 = self.cameraPath[index % numSegments]
        p3 = self.cameraPath[(index + 25) % numSegments]

        n1 = glm.normalize(Core.rotateY90(p2 - p1))
        n2 = glm.normalize(Core.rotateY90(p3 - p2))

        n = glm.slerp(n1, n2, 0.5)

        return n

    def updateMatrices(self, aspectRatio):
        elapsedTime = Debug.getElapsedTime()

        if self.cameraPath:
            t = glm.fract(elapsedTime * 0.01)
            numSegments = len(self.cameraPath)

            segmentStartIndex = int(glm.floor(t * numSegments))
            segmentEndIndex = int(glm.ceil(t * numSegments))

            segmentStartPos = self.cameraPath[segmentStartIndex]
            segmentEndPos = self.cameraPath[segmentEndIndex % numSegments]

            segmentStartNormal = self.getCameraPathNormalAtIndex(segmentStartIndex)
            segmentEndNormal = self.getCameraPathNormalAtIndex(segmentEndIndex)

            segmentT = Core.inverseLerp(segmentStartIndex, segmentEndIndex, t * numSegments)

            self.position = glm.lerp(segmentStartPos, segmentEndPos, segmentT)
            self.forward = glm.slerp(segmentStartNormal, segmentEndNormal, segmentT)

        #alpha = elapsedTime * 0.2
        #self.forward = glm.vec3(glm.cos(alpha), 0, glm.sin(alpha))

        self.projectionTransform = glm.perspective(glm.radians(self.fov), aspectRatio, 0.1, 1000.0)

        self.viewTransform = glm.lookAt(self.position, self.position + self.forward, self.up)