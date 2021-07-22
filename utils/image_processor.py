import cv2
import pytesseract


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
            s = pytesseract.image_to_string(cropped).strip()
            results.append(((x, y, x + w, y + h), s))
        return results
