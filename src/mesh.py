from pathlib import Path
import pickle
from hashlib import sha256

import moderngl as gl
import numpy as np
from pygltflib import GLTF2
from pygltflib import Primitive as gltfPrimitive, Accessor as gltfAccessor, BufferView as gltfBufferView, Material as gltfMaterial, Texture as gltfTexture

from core import Core
from material import Material

class MeshPart:
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
    def readBuffer(buffer: bytes, bufferView: gltfBufferView, accessor: gltfAccessor):
        viewedBuffer = buffer[bufferView.byteOffset : (bufferView.byteOffset + bufferView.byteLength) : bufferView.byteStride]

        if accessor.byteOffset:
            byteLength = np.dtype(MeshPart.componentTypeMapping[accessor.componentType]).itemsize * MeshPart.numElementsMapping[accessor.type] * accessor.count
            return viewedBuffer[accessor.byteOffset : (accessor.byteOffset + byteLength)]
        else:
            return viewedBuffer
    
    @staticmethod
    def createArrayFromBytes(buffer: bytes, accessor: gltfAccessor):
        return np.frombuffer(buffer, dtype = MeshPart.componentTypeMapping[accessor.componentType])

    def __init__(self, gltf: GLTF2, buffer: bytes, primitive: gltfPrimitive):
        self.glContext = gl.get_context()

        positionAccessor: gltfAccessor = gltf.accessors[primitive.attributes.POSITION]
        normalAccessor: gltfAccessor = gltf.accessors[primitive.attributes.NORMAL]
        uvAccessor: gltfAccessor = gltf.accessors[primitive.attributes.TEXCOORD_0]
        indexAccessor: gltfAccessor = gltf.accessors[primitive.indices]

        positionBufferView: gltfBufferView = gltf.bufferViews[positionAccessor.bufferView]
        normalBufferView: gltfBufferView = gltf.bufferViews[normalAccessor.bufferView]
        uvBufferView: gltfBufferView = gltf.bufferViews[uvAccessor.bufferView]
        indexBufferView: gltfBufferView = gltf.bufferViews[indexAccessor.bufferView]

        vertexDataBytes = MeshPart.readBuffer(buffer, positionBufferView, positionAccessor)
        normalDataBytes = MeshPart.readBuffer(buffer, normalBufferView, normalAccessor)
        uvDataBytes = MeshPart.readBuffer(buffer, uvBufferView, uvAccessor)
        indexDataBytes = MeshPart.readBuffer(buffer, indexBufferView, indexAccessor)

        vertexData = MeshPart.createArrayFromBytes(vertexDataBytes, positionAccessor)
        normalData = MeshPart.createArrayFromBytes(normalDataBytes, normalAccessor)
        uvData = MeshPart.createArrayFromBytes(uvDataBytes, uvAccessor)
        indexData = MeshPart.createArrayFromBytes(indexDataBytes, indexAccessor)

        self.positionVbo = self.glContext.buffer(np.asarray(vertexData, dtype = np.float32).tobytes())
        self.normalVbo = self.glContext.buffer(np.asarray(normalData, dtype = np.float32).tobytes())
        self.uvVbo = self.glContext.buffer(np.asarray(uvData, dtype = np.float32).tobytes())
        self.ibo = self.glContext.buffer(np.asarray(indexData, dtype = np.int32).tobytes())

        self.material = Material("shaders/basicVertexShader.glsl", "shaders/basicFragmentShader.glsl")

        self.vao = self.glContext.vertex_array(self.material.shaderProgram, [
            (self.positionVbo, "3f", "in_position"),
            (self.normalVbo, "3f", "in_normal"),
            (self.uvVbo, "2f", "in_uv"),
        ], index_buffer = self.ibo)

        #material: gltfMaterial = gltf.materials[primitive.material]
        #baseColorTexture: gltfTexture = gltf.textures[material.pbrMetallicRoughness.baseColorTexture]
        #metallicRoughnessTexture: gltfTexture = gltf.textures[material.pbrMetallicRoughness.metallicRoughnessTexture]
    
    def render(self):
        self.vao.render()

class Mesh:
    def __init__(self, gltf: GLTF2, buffer: bytes, primitives: list[gltfPrimitive]):
        self.glContext = gl.get_context()
        
        # modelPath = Core.getPath(relativePath)

        # with open(modelPath, "rb") as modelFile:
        #     modelData = modelFile.read()
        #     modelHash = sha256(modelData).hexdigest()

        # cachedModelPath = Path(Core.getPath(f"cache/{Path(relativePath).name}.cache"))
        # wasCacheUsed = False

        # if cachedModelPath.exists():
        #     with open(cachedModelPath, "rb") as cachedModelFile:
        #         cachedModelData: tuple[int, tuple[list, list, list]] = pickle.load(cachedModelFile)
        #         cachedModelHash, cachedModel = cachedModelData

        #         if cachedModelHash == modelHash:
        #             wasCacheUsed = True
        #             uniqueVertices, vertexIndices = cachedModel
        #             print("Using cached file.")

        #         else:
        #             print("Cached file has different hash, cache will not be used.")
                
        # else:
        #     print("Cached file does not exist.")

        # if not wasCacheUsed:
        #     print("Cache could not be used.")

        #     print("Loading model... This could take a while.")
        #     model = load_model(modelPath)

        #     allVertexPosition = [tuple(model.vertex_points[positionIndex].tolist()) for triangleIndices in model.point_indices for positionIndex in triangleIndices]
        #     allVertexNormals = [tuple(model.vertex_normals[normalIndex].tolist()) for triangleIndices in model.normal_indices for normalIndex in triangleIndices]
        #     allVertexUvs = [tuple(model.vertex_uv[uvIndex].tolist()) for triangleIndices in model.uv_indices for uvIndex in triangleIndices]

        #     allVertexData = [(*allVertexPosition[i], *allVertexNormals[i], *allVertexUvs[i]) for i in range(len(allVertexPosition))]

        #     uniqueVertexData: dict[tuple, int] = {}

        #     for newVertexData in allVertexData:
        #         if newVertexData not in uniqueVertexData:
        #             uniqueVertexData[newVertexData] = len(uniqueVertexData)

        #     uniqueVertices = list(uniqueVertexData.keys())
        #     vertexIndices = [uniqueVertexData[vertexData] for vertexData in allVertexData]
            
        #     print("Model loaded.")

        #     with open(cachedModelPath, "wb") as cachedModelFile:
        #         print("Cache has been created.")

        #         pickle.dump((modelHash, (uniqueVertices, vertexIndices)), cachedModelFile)

        # self.vbo = self.glContext.buffer(np.array(uniqueVertices, dtype='f4').tobytes())
        # self.ibo = self.glContext.buffer(np.array(vertexIndices, dtype='i4').tobytes())

        self.parts = [MeshPart(gltf, buffer, primitive) for primitive in primitives]

    def render(self):
        for part in self.parts:
            part.render()