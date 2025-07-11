import moderngl as gl

from core import Core
from object import Object, SingleObject
from environment import Environment

class Scene:
    def __init__(self, environment: Environment):
        self.glContext = gl.get_context()

        self.objects: list[SingleObject] = []
        self.environment = environment
    
    def render(self):
        self.environment.render()

        for object in self.objects:
            object.render()
        
    def addObject(self, object):
        self.objects.append(object)