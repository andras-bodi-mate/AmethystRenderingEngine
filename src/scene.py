from pathlib import Path

import moderngl as gl
from pygltflib import GLTF2
from pygltflib import Mesh as gltfMesh, Node as gltfNode
from pyglm import glm

from core import Core
from object import Object, SingleObject
from mesh import Mesh
from material import Material
from transform import Transform

class Scene:
    def __init__(self, path):
        self.glContext = gl.get_context()

        self.objects: list[SingleObject] = []

        gltf = GLTF2().load(Core.getPath(path))
        with open(Core.getPath(path).parent / gltf.buffers[0].uri, "rb") as bufferFile:
            buffer = bufferFile.read()

        mainScene = gltf.scenes[gltf.scene]
        loadedObjectIndices: dict[int, Object] = {}

        # TODO: abstract loading away into separate class
        def loadNode(nodeIndex, parentIndex: int | None = None):
            node: gltfNode = gltf.nodes[nodeIndex]
            mesh: gltfMesh = gltf.meshes[node.mesh] if node.mesh else None

            transform = Transform(node.matrix) if node.matrix else Transform.fromTranslationRotationScale(
                glm.vec3(*node.translation) if node.translation else glm.vec3(0),
                glm.quat(node.rotation[3], node.rotation[0], node.rotation[1], node.rotation[2]) if node.rotation else glm.quat(),
                glm.vec3(*node.scale) if node.scale else glm.vec3(1)
            )

            newObject = SingleObject(Mesh(gltf, buffer, mesh.primitives) if mesh and mesh.primitives else None, transform, node.name)
            loadedObjectIndices[nodeIndex] = newObject

            if parentIndex:
                loadedObjectIndices[parentIndex].children.append(newObject)
            else:
                self.objects.append(newObject)

            if node.children:
                for childIndex in node.children:
                    loadNode(childIndex, nodeIndex)

        for nodeIndex in mainScene.nodes:
            loadNode(nodeIndex)
    
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