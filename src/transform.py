from pyglm import glm

from core import Core

class Transform:
    @staticmethod
    def fromTranslationRotationScale(translation: glm.vec3, rotation: glm.quat, scale: glm.vec3):
        return Transform().translated(translation).rotated(rotation).scaled(scale)
        
    def __init__(self, transformation: glm.mat4x4 = glm.identity(glm.mat4x4)):
        self.transformation = transformation

    def translated(self, translation: glm.vec3):
        return Transform(glm.translate(self.transformation, translation))

    def translate(self, translation: glm.vec3):
        self.transformation = self.translated(translation).transformation

    def rotated(self, rotation: glm.quat):
        return Transform(self.transformation * glm.mat4_cast(rotation))

    def rotate(self, rotation: glm.quat):
        self.transformation = self.rotated(rotation).transformation

    def scaled(self, scale: glm.vec3 | float):
        if isinstance(scale, float):
            scale = glm.vec3(scale)
        
        return Transform(glm.scale(self.transformation, scale))
    
    def scale(self, scale: glm.vec3 | float):
        self.transformation = self.scaled(scale).transformation

    
    def getTranslation(self):
        return glm.vec3(self.transformation[Core.convertMatrixIndex(3, 0)],
                        self.transformation[Core.convertMatrixIndex(3, 1)],
                        self.transformation[Core.convertMatrixIndex(3, 2)]
        )