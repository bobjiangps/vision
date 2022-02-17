import cv2
import pytesseract as ptr


class Imager:

    @classmethod
    def recognize_contours(cls, img, font="small"):
        rk_size = {
            "small": (18, 18),
            "large": (36, 36)
        }
        img = cv2.imread(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rk_size[font.lower()])
        dilation = cv2.dilate(thresh, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        img_copy = img.copy()
        results = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cropped = img_copy[y:y + h, x:x + w]
            s = ptr.image_to_string(cropped).strip()
            results.append(((x, y, x + w, y + h), s))
        return results, img.shape

    @classmethod
    def recognize_crop_contours(cls, img, crop, expand=20):
        result = cls.crop_contours(img, crop)
        if result == "":
            crop = (crop[0]-expand, crop[1]-expand, crop[2]+expand, crop[3]+expand)
            return cls.crop_contours(img, crop)
        else:
            return result

    @classmethod
    def crop_contours(cls, img, crop):
        img = cv2.imread(img)
        crop_img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
        result = ptr.image_to_string(crop_img).strip()
        if result == "":
            crop_img = cv2.bitwise_not(crop_img)
            _, binary = cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)
            result = ptr.image_to_string(binary, config="--oem 3 --psm 6").strip()
        return result
