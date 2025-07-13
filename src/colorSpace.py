import numpy as np

class ColorSpace:
    @staticmethod
    def convertSrgbToLinear(c):
        np.where(c <= 0.04045,
                 c / 12.92,
                 ((c + 0.055) / 1.055) ** 2.4)