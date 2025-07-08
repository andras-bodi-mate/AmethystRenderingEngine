from pathlib import Path

import cv2
import numpy as np

from core import Core

class Image:
    @staticmethod
    def open(path: Path | str, dataType = np.uint8, flipVertical = False):
        if Path(path).exists():
            cvImage = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        else:
            cvImage = cv2.imread(Core.getPath(Path(path)), cv2.IMREAD_UNCHANGED)

        if flipVertical:
            cvImage = cv2.flip(cvImage, 0)

        return Image(np.asarray(cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB), dtype = dataType))

    def __init__(self, data: np.ndarray):
        self.data = data

    @property
    def size(self):
        return self.data.shape[:2]
    
    @property
    def dataType(self):
        return self.data.dtype
    
    @property
    def numComponents(self):
        return self.data.shape[2] if self.data.ndim == 3 else 1
    
    def toBytes(self):
        return self.data.tobytes()