import moderngl as gl
import numpy as np
from pyobjloader import load_model

from core import Core

class Mesh:
    def __init__(self, path):
        self.glContext = gl.get_context()

        self.model = load_model(Core.getPath(path))

        allVertexPosition = [tuple(self.model.vertex_points[positionIndex].tolist()) for triangleIndices in self.model.point_indices for positionIndex in triangleIndices]
        allVertexNormals = [tuple(self.model.vertex_normals[normalIndex].tolist()) for triangleIndices in self.model.normal_indices for normalIndex in triangleIndices]
        #allVertexUvs = [tuple(self.model.vertex_uv[uvIndex].tolist()) for uvIndex in self.model.uv_indices]

        allVertexData = [(allVertexPosition[i], allVertexNormals[i]) for i in range(len(allVertexPosition))]

        uniqueVertexData = {}

        for newVertexData in allVertexData:
            if newVertexData not in uniqueVertexData:
                uniqueVertexData[newVertexData] = len(uniqueVertexData)

        vertexIndices = [uniqueVertexData[vertexData] for vertexData in allVertexData]

        self.vbo = self.glContext.buffer(np.array(list(uniqueVertexData.keys()), dtype='f4').tobytes())

        self.ibo = self.glContext.buffer(np.array(vertexIndices, dtype='i4').tobytes())