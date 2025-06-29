from pathlib import Path

import moderngl as gl
from pygltflib import GLTF2
from pygltflib import Mesh as gltfMesh

from core import Core
from object import SingleObject
from mesh import Mesh
from material import Material

class Scene:
    def __init__(self, path):
        self.glContext = gl.get_context()

        self.objects: list[SingleObject] = []

        gltf = GLTF2().load(Core.getPath(path))
        with open(Core.getPath(path).parent / gltf.buffers[0].uri, "rb") as bufferFile:
            buffer = bufferFile.read()

        mainScene = gltf.scenes[gltf.scene]

        for nodeIndex in mainScene.nodes:
            node = gltf.nodes[nodeIndex]
            mesh: gltfMesh = gltf.meshes[node.mesh]

            newObject = SingleObject(Mesh(gltf, buffer, mesh.primitives))

            self.objects.append(newObject)
    
    def render(self):
        self.glContext.enable(self.glContext.DEPTH_TEST)

        for object in self.objects:
            object.render()
        
    def addObject(self, object):
        self.objects.append(object)

    #def updateViewTransformUniforms(self, viewTransform):
    #    for object in self.objects:
    #        object.material.shaderProgram["viewTransform"].write(viewTransform)

    #def updatePerspectiveTransformUniforms(self, perspectiveTransform):
    #    for object in self.objects:
    #        object.material.shaderProgram["perspectiveTransform"].write(perspectiveTransform)