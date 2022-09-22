import glob
import os
import cv2
import numpy as np
from pathlib import Path
from lib.visual.augment import letterbox
from conf.config import LoadConfig


class LoadImages:
    def __init__(self, path, img_size=640, stride=32):
        p = str(Path(path).absolute())
        if '*' in p:
            files = sorted(glob.glob(p, recursive=True))
        elif os.path.isdir(p):
            files = sorted(glob.glob(os.path.join(p, '*.*')))
        elif os.path.isfile(p):
            files = [p]
        else:
            raise Exception(f'ERROR: {p} does not exist')
        img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']
        # vid_formats = ['mov', 'avi', 'mp4', 'mpg', 'mpeg', 'm4v', 'wmv', 'mkv']
        images = [x for x in files if x.split('.')[-1].lower() in img_formats]
        # videos = [x for x in files if x.split('.')[-1].lower() in vid_formats]
        # ni, nv = len(images), len(videos)

        self.img_size = img_size
        self.stride = stride
        # self.files = images + videos
        self.files = images
        # self.nf = ni + nv
        self.nf = len(images)
        # self.video_flag = [False] * ni + [True] * nv
        self.mode = 'image'
        # if any(videos):
        #     self.new_video(videos[0])
        # else:
        #     self.cap = None
        assert self.nf > 0, f'No images or videos found in {p}. ' \
                            f'Supported formats are:\nimages: {img_formats}\nvideos: {vid_formats}'

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count == self.nf:
            raise StopIteration
        path = self.files[self.count]

        # if self.video_flag[self.count]:
        #     self.mode = 'video'
        #     ret_val, img0 = self.cap.read()
        #     if not ret_val:
        #         self.count += 1
        #         self.cap.release()
        #         if self.count == self.nf:
        #             raise StopIteration
        #         else:
        #             path = self.files[self.count]
        #             self.new_video(path)
        #             ret_val, img0 = self.cap.read()
        #
        #     self.frame += 1
        #     # print(f'video {self.count + 1}/{self.nf} ({self.frame}/{self.frames}) {path}: ', end='')
        #
        # else:
        #     self.count += 1
        #     img0 = cv2.imread(path)
        #     assert img0 is not None, 'Image Not Found ' + path
        #     # print(f'image {self.count}/{self.nf} {path}: ', end='')

        self.count += 1
        img0 = cv2.imread(path)

        pad = self.check_pad(img0)
        pad = pad if pad < 200 else 200
        LoadConfig().model["pad"] = pad
        img0 = img0[:, pad:-pad]

        assert img0 is not None, 'Image Not Found ' + path

        img = letterbox(img0, self.img_size, stride=self.stride)[0]
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)

        # return path, img, img0, self.cap
        return path, img, img0

    # def new_video(self, path):
    #     self.frame = 0
    #     self.cap = cv2.VideoCapture(path)
    #     self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    @staticmethod
    def check_pad(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, 0]], np.float32)
        dst = cv2.filter2D(gray, -1, kernel)
        canny = cv2.Canny(dst, 30, 200, 1)
        cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = list(cnts)
        left = None
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if left is None:
                left = x
            else:
                if x < left and x != 0:
                    left = x
        return left

    def __len__(self):
        return self.nf
