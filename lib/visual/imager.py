from paddleocr import PaddleOCR
from lib.singleton import Singleton
from conf.config import LoadConfig
from pathlib import Path
import zipfile
import cv2
import shutil
import requests


class Imager(Singleton):

    _PO = None

    @classmethod
    def recognize_contours(cls, img, **kwargs):
        if not cls._PO:
            cls.activate_po()
        img = cv2.imread(img)
        results = []
        for r in cls._PO.ocr(img, cls=False):
            results.append(((r[0][0][0], r[0][0][1], r[0][2][0], r[0][2][1]), r[1][0]))
            if len(r[1][0]) > 120:
                img2 = img[r[0][0][1] + 20:r[0][2][1] - 20, r[0][0][0] + 20:r[0][2][0] - 20]
                for r2 in cls._PO.ocr(img2, cls=False):
                    results.insert(-1, ((r2[0][0][0], r2[0][0][1], r2[0][2][0], r2[0][2][1]), r2[1][0]))
        return results, img.shape

    @classmethod
    def recognize_crop_contours(cls, img, crop, expand=10):
        if not cls._PO:
            cls.activate_po()
        result = cls.crop_contours(img, crop)
        if result == "":
            try:
                crop = (crop[0]-expand, crop[1]-expand, crop[2]+expand, crop[3]+expand)
                return cls.crop_contours(img, crop)
            except TypeError:
                return result
        else:
            return result

    @classmethod
    def crop_contours(cls, img, crop):
        img = cv2.imread(img)
        crop_img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
        r = cls._PO.ocr(crop_img, cls=False)
        return r[0][1][0] if len(r) > 1 else ""

    @classmethod
    def activate_po(cls, lang_code="en", latest=False, remove=False):
        if latest:
            cls._PO = PaddleOCR(use_angle_cls=False, lang=lang_code, show_log=False)
            return True
        resource_folder = Path.cwd().joinpath("resource", "paddle")
        if remove and resource_folder.exists():
            shutil.rmtree(resource_folder)
        if not resource_folder.exists():
            r = requests.get(f"{LoadConfig().remote}/ocr/paddle.zip")
            temp = Path.cwd().joinpath("resource", "paddle.zip")
            if r.status_code == 200:
                with open(temp, "wb") as f:
                    f.write(r.content)
                with zipfile.ZipFile(str(temp), "r") as z:
                    z.extractall(str(Path.cwd().joinpath("resource")))
                temp.unlink()
        cls._PO = PaddleOCR(use_angle_cls=False,
                            lang=lang_code,
                            show_log=False,
                            cls_model_dir=str(Path.cwd().joinpath("resource", "paddle", "cls", "ch_ppocr_mobile_v2.0_cls_infer")),
                            det_model_dir=str(Path.cwd().joinpath("resource", "paddle", "det", lang_code, "en_PP-OCRv3_det_infer")),
                            rec_model_dir=str(Path.cwd().joinpath("resource", "paddle", "rec", lang_code, "en_PP-OCRv3_rec_infer")))


# import cv2
# import pytesseract as ptr
# import platform
#
#
# class Imager:
#
#     @classmethod
#     def recognize_contours(cls, img, font="small"):
#         img = cv2.imread(img)
#         contours = cls.contours(img, font)
#         img_copy = img.copy()
#         results = []
#         for cnt in contours:
#             x, y, w, h = cv2.boundingRect(cnt)
#             cropped = img_copy[y:y + h, x:x + w]
#             s = ptr.image_to_string(cropped).strip()
#             results.append(((x, y, x + w, y + h), s))
#             if len(s) > 120:
#                 img2 = img[y+20:y+h-20, x+20:x+w-20]
#                 contours2 = cls.contours(img2, font)
#                 img_copy2 = img2.copy()
#                 for cnt2 in contours2:
#                     x2, y2, w2, h2 = cv2.boundingRect(cnt2)
#                     cropped2 = img_copy2[y2:y2 + h2, x2:x2 + w2]
#                     s2 = ptr.image_to_string(cropped2).strip()
#                     results.insert(-1, ((x+x2-20, y+y2-20, x+x2+w2+20, y+y2+h2+20), s2))
#         return results, img.shape
#
#     @classmethod
#     def contours(cls, img, font):
#         if platform.platform().lower().find("windows") >= 0:
#             ck_size = {
#                 "small": (14, 14),
#                 "large": (28, 28)
#             }
#         else:
#             ck_size = {
#                 "small": (16, 16),
#                 "large": (32, 32)
#             }
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#         rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ck_size[font.lower()])
#         dilation = cv2.dilate(thresh, rect_kernel, iterations=1)
#         contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#         return contours
#
#     # @classmethod
#     # def recognize_contours(cls, img, font="small"):
#     #     ck_size = {
#     #         "small": (18, 18),
#     #         "large": (36, 36)
#     #     }
#     #     img = cv2.imread(img)
#     #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     #     ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#     #     rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ck_size[font.lower()])
#     #     dilation = cv2.dilate(thresh, rect_kernel, iterations=1)
#     #     contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     #     img_copy = img.copy()
#     #     results = []
#     #     for cnt in contours:
#     #         x, y, w, h = cv2.boundingRect(cnt)
#     #         cropped = img_copy[y:y + h, x:x + w]
#     #         s = ptr.image_to_string(cropped).strip()
#     #         results.append(((x, y, x + w, y + h), s))
#     #     return results, img.shape
#
#     @classmethod
#     def recognize_crop_contours(cls, img, crop, expand=20):
#         result = cls.crop_contours(img, crop)
#         if result == "":
#             try:
#                 crop = (crop[0]-expand, crop[1]-expand, crop[2]+expand, crop[3]+expand)
#                 return cls.crop_contours(img, crop)
#             except TypeError:
#                 return result
#         else:
#             return result
#
#     @classmethod
#     def crop_contours(cls, img, crop):
#         # todo: notice some different bg color and text color like blue bg and white text
#         img = cv2.imread(img)
#         crop_img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
#         crop_img = cv2.bitwise_not(crop_img)
#         _, binary = cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)
#         result = ptr.image_to_string(binary, config="--oem 3 --psm 4").strip()
#         for s in [")", "]", "}"]:
#             if result.find(s) >= 0:
#                 crop_img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
#                 result = ptr.image_to_string(crop_img).strip()
#         return result
#         # img = cv2.imread(img)
#         # crop_img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
#         # result = ptr.image_to_string(crop_img).strip()
#         # flag = False
#         # special = ["NV", "¢", "] "]
#         # for s in special:
#         #     if result.find(s) >= 0:
#         #         flag = True
#         #         break
#         # if result == "" or flag:
#         #     crop_img = cv2.bitwise_not(crop_img)
#         #     _, binary = cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)
#         #     result = ptr.image_to_string(binary, config="--oem 3 --psm 6").strip()
#         #     if result == "":
#         #         result = ptr.image_to_string(binary, config="--psm 10").strip()
#         # return result
