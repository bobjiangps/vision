import cv2
import pytesseract as ptr


class ImageProcessor:

    @classmethod
    def recognize_contours(cls, img):
        img = cv2.imread(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
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
    def recognize_crop_contours(cls, img, crop):
        img = cv2.imread(img)
        crop_img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
        return ptr.image_to_string(crop_img).strip()