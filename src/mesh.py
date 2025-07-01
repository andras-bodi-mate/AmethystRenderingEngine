from pathlib import Path
import pickle
from hashlib import sha256

import moderngl as gl
import numpy as np
from numpy.lib.stride_tricks import as_strided
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
    def readBuffer(buffer: memoryview, bufferView: gltfBufferView, accessor: gltfAccessor):
        componentDataType = MeshPart.componentTypeMapping[accessor.componentType]
        elementSize = np.dtype(componentDataType).itemsize * MeshPart.numElementsMapping[accessor.type]

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

            stridedArray = as_strided(
                viewedArray,
                shape = (numElements, elementSize),
                strides = (bufferView.byteStride, 1),  # move by `byteStride` bytes for each row, 1 byte per column
                writeable = False
            )

            viewedBuffer = stridedArray.reshape(-1).tobytes()

        if accessor.byteOffset:
            byteLength = elementSize * accessor.count
            return viewedBuffer[accessor.byteOffset : (accessor.byteOffset + byteLength)]
        else:
            return viewedBuffer
    
    @staticmethod
    def createArrayFromBytes(buffer: bytes, accessor: gltfAccessor):
        return np.frombuffer(buffer, dtype = MeshPart.componentTypeMapping[accessor.componentType])

    def __init__(self, gltf: GLTF2, buffer: bytes, primitive: gltfPrimitive, material):
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

        self.material = material

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
    def __init__(self, gltf: GLTF2, buffer: bytes, primitives: list[gltfPrimitive], material):
        self.glContext = gl.get_context()

        self.parts = [MeshPart(gltf, buffer, primitive, material) for primitive in primitives]

    def render(self):
        for part in self.parts:
            part.render()