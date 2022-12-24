from lib.singleton import Singleton
from conf.config import LoadConfig
from pathlib import Path
import numpy as np
import cv2


class Grad(Singleton):

    _img = str(Path.cwd().joinpath("resource", "img", f"{LoadConfig().model['img']}.png"))

    @classmethod
    def narrow(cls, border, coefficient=0.35):
        img = cv2.imread(cls._img)
        origin = img[border[1]:border[3], border[0]:border[2]].copy()
        w_ratio = (border[2] - border[0]) * coefficient
        h_ratio = (border[3] - border[1]) * coefficient
        change = img[(border[1]+int(h_ratio)):(border[3]-int(h_ratio)), (border[0]+int(w_ratio)):(border[2]-int(w_ratio))].copy()
        return np.average(origin, axis=(0, 1)), np.average(change, axis=(0, 1))
