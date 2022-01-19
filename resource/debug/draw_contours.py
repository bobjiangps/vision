import cv2
import pytesseract as ptr


img = cv2.imread('./resource/img/page.png')
# # crop = (915, 953, 1534, 1035)
# crop = (373, 898, 1228, 1017)
# img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
dilation = cv2.dilate(thresh, rect_kernel, iterations=1)
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
img_copy = gray.copy()
results = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cropped = img_copy[y:y + h, x:x + w]
    s = ptr.image_to_string(cropped).strip()
    results.append(((x, y, x + w, y + h), s))
print(results)
# crop = (1846, 51, 2217, 149)
# # crop = (915, 953, 1534, 1035)
# part_img = gray[crop[1]:crop[3], crop[0]:crop[2]].copy()
# print(ptr.image_to_string(part_img))
cv2.drawContours(image=img_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                 lineType=cv2.LINE_AA)
cv2.imshow('None approximation', img_copy)
cv2.imwrite('contours_none_image1.jpg', img_copy)
while True:
    user_input = cv2.waitKey(3000)
    if user_input == ord('q'):
        break
cv2.destroyAllWindows()



# import cv2
# import pytesseract
#
# img = cv2.imread("./resource/img/page.png")
# # crop = (1823, 77, 2209, 160)
# crop = (373, 898, 1228, 1017)
# img = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
# txt = pytesseract.image_to_string(img).strip()
# print(txt)
# print(txt.strip()=="")
# if txt == "":
#     img = cv2.bitwise_not(img)
#     _, binary = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
#     txt = pytesseract.image_to_string(binary, config="--oem 3 --psm 4")
# print(txt)
# print(txt.strip()=="")
