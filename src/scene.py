import moderngl as gl

from core import Core
from object import Object, SingleObject
from environmentMap import EnvironmentMap
from environment import Environment
from image import Image

class Scene:
    def __init__(self):
        self.glContext = gl.get_context()

        self.objects: list[SingleObject] = []
        self.environment = Environment(EnvironmentMap("res/environments/mountain.hdr"))
    
    def render(self):
        self.glContext.enable(self.glContext.DEPTH_TEST)

        self.environment.render()

        for object in self.objects:
            object.render()
        
    def addObject(self, object):
        self.objects.append(object)