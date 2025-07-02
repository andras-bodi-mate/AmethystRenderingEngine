import moderngl as gl

from core import Core
from object import Object, SingleObject

class Scene:
    def __init__(self):
        self.glContext = gl.get_context()

        self.objects: list[SingleObject] = []
    
    def render(self):
        self.glContext.enable(self.glContext.DEPTH_TEST)

        for object in self.objects:
            object.render()
        
    def addObject(self, object):
        self.objects.append(object)