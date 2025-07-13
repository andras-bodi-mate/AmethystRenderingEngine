from pathlib import Path

import cv2
import numpy as np
from pyglm import glm

from core import Core
from colorSpace import ColorSpace

class Image:
    @staticmethod
    def open(path: Path | str, dataType = np.uint8, flipVertical = False, isSrgb = False):
        if Path(path).exists():
            image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        else:
            image = cv2.imread(Core.getPath(Path(path)), cv2.IMREAD_UNCHANGED)

        if flipVertical:
            image = cv2.flip(image, 0)

        image = np.asarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), dtype = dataType)

        if isSrgb:
            ColorSpace.convertSrgbToLinear(image)

        return Image(image)

    def __init__(self, data: np.ndarray):
        self.data = data

    @property
    def size(self):
        size = self.data.shape[:2]
        return glm.ivec2(size[0], size[1])
    
    @property
    def dataType(self):
        return self.data.dtype
    
    @property
    def numComponents(self):
        return self.data.shape[2] if self.data.ndim == 3 else 1
    
    def toBytes(self):
        return self.data.tobytes()