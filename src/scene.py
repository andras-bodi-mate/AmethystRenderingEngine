import moderngl as gl

from object import Object

class Scene:
    def __init__(self):
        self.glContext = gl.get_context()

        self.objects: list[Object] = []
    
    def draw(self):
        self.glContext.multisample = True
        self.glContext.enable(self.glContext.DEPTH_TEST)

        for object in self.objects:
            object.draw()
        
    def addObject(self, object):
        self.objects.append(object)

    def updateViewTransformUniforms(self, viewTransform):
        for object in self.objects:
            object.material.shaderProgram["viewTransform"].write(viewTransform)

    def updatePerspectiveTransformUniforms(self, perspectiveTransform):
        for object in self.objects:
            object.material.shaderProgram["perspectiveTransform"].write(perspectiveTransform)