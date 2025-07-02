from pathlib import Path

from pyglm import glm
from pygltflib import GLTF2, Scene as GltfScene, Node as GltfNode, Mesh as GltfMesh, Material as GltfMaterial, Texture as GltfTexture, Image as GltfImage, Sampler as GltfSampler, BufferView as GltfBufferView, Accessor as GltfAccessor, Primitive as GltfPrimitive
import moderngl as gl
from PIL import Image
import numpy as np

from core import Core
from scene import Scene
from object import Object, SingleObject
from mesh import Mesh, MeshPart
from material import Material
from texture import Texture, Sampler
from transform import Transform

class GltfLoader:
    magnificationFilterMapping = {
        9728: gl.NEAREST,
        9729: gl.LINEAR
    }

    minificationFilterMapping = {
        9728: gl.NEAREST,
        9729: gl.LINEAR,
        9984: gl.NEAREST_MIPMAP_NEAREST,
        9985: gl.LINEAR_MIPMAP_NEAREST,
        9986: gl.NEAREST_MIPMAP_LINEAR,
        9987: gl.LINEAR_MIPMAP_LINEAR
    }

    repeatModeMapping = {
        33071: False,
        33648: True,
        10497: True
    }

    componentTypeMapping = {
        5120: np.int8,
        5121: np.uint8,
        5122: np.int16,
        5123: np.uint16,
        5125: np.uint32,
        5126: np.float32
    }

    numElementsMapping = {
        "SCALAR": 1,
        "VEC2": 2,
        "VEC3": 3,
        "VEC4": 4,
        "MAT2": 4,
        "MAT3": 9,
        "MAT4": 16
    }

    @staticmethod
    def readBuffer(buffer: memoryview, bufferView: GltfBufferView, accessor: GltfAccessor):
        componentDataType = GltfLoader.componentTypeMapping[accessor.componentType]
        elementSize = np.dtype(componentDataType).itemsize * GltfLoader.numElementsMapping[accessor.type]

        viewedBuffer = buffer[bufferView.byteOffset : (bufferView.byteOffset + bufferView.byteLength)]

        if bufferView.byteStride and bufferView.byteStride != elementSize:
            viewedBuffer = buffer[bufferView.byteOffset : (bufferView.byteOffset + bufferView.byteLength)]
            viewedArray = np.frombuffer(viewedBuffer, dtype = np.uint8)

            numElements = (bufferView.byteLength - elementSize) // bufferView.byteStride + 1
            if numElements <= 0:
                raise ValueError("Cannot fit even one element within the buffer given the stride, element size and buffer length")

            # stridedBuffer = bytearray(numElements * elementSize)
            # for i in range(numElements - 1):
            #     start = i * bufferView.byteStride
            #     end = start + elementSize
            #     stridedBuffer[i * elementSize : (i + 1) * elementSize] = viewedBuffer[start : end]

            stridedArray = np.lib.stride_tricks.as_strided(
                viewedArray,
                shape = (numElements, elementSize),
                strides = (bufferView.byteStride, 1),
                writeable = False
            )

            viewedBuffer = stridedArray.reshape(-1).tobytes()

        if accessor.byteOffset:
            byteLength = elementSize * accessor.count
            return viewedBuffer[accessor.byteOffset : (accessor.byteOffset + byteLength)]
        else:
            return viewedBuffer
    
    @staticmethod
    def createArrayFromBytes(buffer: bytes, accessor: GltfAccessor):
        return np.frombuffer(buffer, dtype = GltfLoader.componentTypeMapping[accessor.componentType])

    def __init__(self):
        pass

    def loadTexture(self, gltfTexture: GltfTexture, color: list[float] | None = None):
        #sampler: Sampler = self.loadSampler(self.gltf.samplers[gltfTexture.sampler] )
        gltfSampler: GltfSampler = self.gltf.samplers[gltfTexture.sampler] if gltfTexture else None

        if gltfTexture:
            minificationFilter = GltfLoader.minificationFilterMapping[gltfSampler.minFilter]
            magnificationFilter = GltfLoader.magnificationFilterMapping[gltfSampler.magFilter]
            doRepeatX = GltfLoader.repeatModeMapping[gltfSampler.wrapS]
            doRepeatY = GltfLoader.repeatModeMapping[gltfSampler.wrapT]

        else:
            minificationFilter = gl.LINEAR
            magnificationFilter = gl.LINEAR
            doRepeatX = False
            doRepeatY = False

        if gltfTexture:
            gltfImage: GltfImage = self.gltf.images[gltfTexture.source]

            with Image.open(self.gltfDir / Path(gltfImage.uri)).convert("RGB") as image:
                return Texture(image, minificationFilter, magnificationFilter, doRepeatX, doRepeatY)
            
        else:
            print("from color")
            return Texture.fromColor(glm.vec3(color), minificationFilter, magnificationFilter, doRepeatX, doRepeatY)

    def loadMaterial(self, gltfMaterial: GltfMaterial):
        pbr = gltfMaterial.pbrMetallicRoughness

        baseColorTexture = self.loadTexture(self.gltf.textures[pbr.baseColorTexture.index] if pbr.baseColorTexture else None, pbr.baseColorFactor)
        #normalTexture = self.loadTexture(self.gltf.textures[gltfMaterial.normalTexture.index])
        #metallicRoughnessTexture = self.loadTexture(self.gltf.textures[pbr.metallicRoughnessTexture.index] if pbr.metallicRoughnessTexture else None, (pbr.metallicFactor, pbr.roughnessFactor, 0))

        print("Loaded material.")

        return Material("shaders/basicVertexShader.glsl", "shaders/basicFragmentShader.glsl", baseColorTexture)

    def loadMeshPart(self, gltfPrimitive: GltfPrimitive):
        positionAccessor: GltfAccessor = self.gltf.accessors[gltfPrimitive.attributes.POSITION]
        normalAccessor: GltfAccessor = self.gltf.accessors[gltfPrimitive.attributes.NORMAL]
        uvAccessor: GltfAccessor = self.gltf.accessors[gltfPrimitive.attributes.TEXCOORD_0]
        indexAccessor: GltfAccessor = self.gltf.accessors[gltfPrimitive.indices]

        positionBufferView: GltfBufferView = self.gltf.bufferViews[positionAccessor.bufferView]
        normalBufferView: GltfBufferView = self.gltf.bufferViews[normalAccessor.bufferView]
        uvBufferView: GltfBufferView = self.gltf.bufferViews[uvAccessor.bufferView]
        indexBufferView: GltfBufferView = self.gltf.bufferViews[indexAccessor.bufferView]

        vertexDataBytes = GltfLoader.readBuffer(self.buffer, positionBufferView, positionAccessor)
        normalDataBytes = GltfLoader.readBuffer(self.buffer, normalBufferView, normalAccessor)
        uvDataBytes = GltfLoader.readBuffer(self.buffer, uvBufferView, uvAccessor)
        indexDataBytes = GltfLoader.readBuffer(self.buffer, indexBufferView, indexAccessor)

        vertexData = np.asarray(GltfLoader.createArrayFromBytes(vertexDataBytes, positionAccessor), dtype = np.float32).tobytes()
        normalData = np.asarray(GltfLoader.createArrayFromBytes(normalDataBytes, normalAccessor), dtype = np.float32).tobytes()
        uvData = np.asarray(GltfLoader.createArrayFromBytes(uvDataBytes, uvAccessor), dtype = np.float32).tobytes()
        indexData = np.asarray(GltfLoader.createArrayFromBytes(indexDataBytes, indexAccessor), dtype = np.int32).tobytes()


        return MeshPart(vertexData, normalData, uvData, indexData, self.materials[gltfPrimitive.material])

    def loadMesh(self, gltfMesh: GltfMesh):
        return Mesh([self.loadMeshPart(gltfPrimitive) for gltfPrimitive in gltfMesh.primitives]) if gltfMesh and gltfMesh.primitives else None

    def loadNode(self, gltfNode: GltfNode):
        mesh: GltfMesh = self.gltf.meshes[gltfNode.mesh] if (gltfNode.mesh is not None) else None

        transform = Transform(gltfNode.matrix) if gltfNode.matrix else Transform.fromTranslationRotationScale(
            glm.vec3(*gltfNode.translation) if gltfNode.translation else glm.vec3(0),
            glm.quat(gltfNode.rotation[3], gltfNode.rotation[0], gltfNode.rotation[1], gltfNode.rotation[2]) if gltfNode.rotation else glm.quat(),
            glm.vec3(*gltfNode.scale) if gltfNode.scale else glm.vec3(1)
        )

        return SingleObject(self.loadMesh(mesh), transform, gltfNode.name)
    
    def loadNodeTree(self, baseNodeIndex: int, parentIndex: int | None = None):
        baseNode: GltfNode = self.gltf.nodes[baseNodeIndex]
        newObject = self.loadNode(baseNode)

        self.loadedObjectIndices[baseNodeIndex] = newObject

        if parentIndex:
            self.loadedObjectIndices[parentIndex].children.append(newObject)
        else:
            self.scene.objects.append(newObject)

        print(f"Successfully loaded node: {newObject.name}")

        if baseNode.children:
            for childIndex in baseNode.children:
                self.loadNodeTree(childIndex, baseNodeIndex)

    def loadScene(self, relativePath: Path):
        path = Core.getPath(relativePath)
        self.gltf = GLTF2().load(path)
        self.gltfDir = path.parent

        with open(self.gltfDir / self.gltf.buffers[0].uri, "rb") as bufferFile:
            self.buffer = memoryview(bufferFile.read())

        self.gltfMainScene: GltfScene = self.gltf.scenes[self.gltf.scene]

        self.scene = Scene()

        self.loadedObjectIndices: dict[int, Object] = {}
        self.materials = [self.loadMaterial(gltfMaterial) for gltfMaterial in self.gltf.materials]

        for nodeIndex in self.gltfMainScene.nodes:
            self.loadNodeTree(nodeIndex)

        return self.scene