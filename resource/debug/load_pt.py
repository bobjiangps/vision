# import cv2
# import torch
# import time
# from models.experimental import attempt_load
# from utils.datasets import LoadImages
# from utils.general import check_img_size, non_max_suppression, scale_coords
# from utils.torch_utils import time_synchronized
# from utils.plots import colors, plot_one_box
#
# if __name__ == "__main__":
#     weights_file = "./resource/models/elements.pt"
#     img_file = "./resource/img/login.jpeg"
#     conf_thres = 0.25
#     iou_thres = 0.45
#     classes = None
#     agnostic_nms = None
#     max_det = 1000
#     line_thickness = 3
#
#     device = torch.device("cpu")
#     model = attempt_load(weights_file, map_location=device)
#     stride = int(model.stride.max())
#     print(stride)
#     imgsz = check_img_size(640, s=stride)
#     print(imgsz)
#     names = model.module.names if hasattr(model, 'module') else model.names
#     print(names)
#     print(len(names))
#     dataset = LoadImages(img_file, img_size=imgsz, stride=stride)
#     bs = 1
#     vid_path, vid_writer = [None] * bs, [None] * bs
#     t0 = time.time()
#     for path, img, im0s, vid_cap in dataset:
#         img = torch.from_numpy(img).to(device)
#         img = img.float()
#         img /= 255.0
#         if img.ndimension() == 3:
#             img = img.unsqueeze(0)
#
#         t1 = time_synchronized()
#         pred = model(img, augment=False, visualize=False)[0]
#         pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
#         t2 = time_synchronized()
#         for i, det in enumerate(pred):
#             p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)
#             if len(det):
#                 det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
#                 for *xyxy, conf, cls in reversed(det):
#                     c = int(cls)
#                     label = f'{names[c]} {conf:.2f}'
#                     print("label: %s" % label)
#                     print((int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])))
#                     plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=line_thickness)
#             print(f'{s}Done. ({t2 - t1:.3f}s)')
#             cv2.imshow(str(p), im0)
#             while True:
#                 user_input = cv2.waitKey(3000)
#                 if user_input == ord('q'):
#                     break
#             cv2.destroyAllWindows()

# ----------------------------------------


# import cv2
# import torch
# import torch.backends.cudnn as cudnn
# import time
#
# from models.experimental import attempt_load
# from utils.datasets import LoadImages
# from utils.general import check_img_size, increment_path, non_max_suppression, scale_coords
# from utils.torch_utils import select_device, load_classifier, time_synchronized
# from utils.plots import colors, plot_one_box
#
# if __name__ == "__main__":
#     weights_file = "./resource/models/elements.pt"
#     img_file = "./resource/img/login.jpeg"
#     conf_thres = 0.33
#     iou_thres = 0.45
#     classes = None
#     agnostic_nms = None
#     max_det = 1000
#     line_thickness = 3
#
#     device = torch.device("cpu")
#     model = attempt_load(weights_file, map_location=device)
#     print(type(model))
#     stride = int(model.stride.max())
#     print(stride)
#     imgsz = check_img_size(640, s=stride)
#     print(imgsz)
#     names = model.module.names if hasattr(model, 'module') else model.names
#     print(names)
#     print(len(names))
#     dataset = LoadImages(img_file, img_size=imgsz, stride=stride)
#     bs = 1
#     vid_path, vid_writer = [None] * bs, [None] * bs
#     t0 = time.time()
#     for path, img, im0s, vid_cap in dataset:
#         img = torch.from_numpy(img).to(device)
#         img = img.float()
#         img /= 255.0
#         if img.ndimension() == 3:
#             img = img.unsqueeze(0)
#
#         t1 = time_synchronized()
#         pred = model(img, augment=False, visualize=False)[0]
#         pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
#         t2 = time_synchronized()
#         for i, det in enumerate(pred):
#             p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)
#             if len(det):
#                 det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
#                 for *xyxy, conf, cls in reversed(det):
#                     c = int(cls)
#                     label = f'{names[c]} {conf:.2f}'
#                     print("label: %s" % label)
#                     print((int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])))
#                     plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=line_thickness)
#             print(f'{s}Done. ({t2 - t1:.3f}s)')
#             cv2.imshow(str(p), im0)
#             while True:
#                 user_input = cv2.waitKey(3000)
#                 if user_input == ord('q'):
#                     break
#             cv2.destroyAllWindows()


import cv2
import torch
import torch.backends.cudnn as cudnn
import time

from models.experimental import attempt_load
from utils.datasets_detect import LoadImages
from utils.general import check_img_size, increment_path, non_max_suppression, scale_coords
from utils.torch_utils import select_device, load_classifier, time_synchronized
from utils.plots import colors, plot_one_box

if __name__ == "__main__":
    weights_file = "./resource/models/elements.pt"
    img_file = "./resource/img/login.jpeg"
    conf_thres = 0.33
    iou_thres = 0.45
    classes = None
    agnostic_nms = None
    max_det = 1000
    line_thickness = 3

    device = torch.device("cpu")
    model = attempt_load(weights_file, map_location=device)
    print(type(model))
    stride = int(model.stride.max())
    print(stride)
    imgsz = check_img_size(640, s=stride)
    print(imgsz)
    names = model.module.names if hasattr(model, 'module') else model.names
    print(names)
    print(len(names))
    dataset = LoadImages(img_file, img_size=imgsz, stride=stride)
    bs = 1
    vid_path, vid_writer = [None] * bs, [None] * bs
    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img_init = cv2.imread(path)
        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        t1 = time_synchronized()
        pred = model(img, augment=False, visualize=False)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        t2 = time_synchronized()
        for i, det in enumerate(pred):
            p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = f'{names[c]} {conf:.2f}'
                    xyxy2 = (xyxy[0]+400, xyxy[1], xyxy[2]+400, xyxy[3])
                    print("label: %s" % label)
                    # print((int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])))
                    # plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=line_thickness)
                    print((int(xyxy2[0]), int(xyxy2[1])), (int(xyxy2[2]), int(xyxy2[3])))
                    plot_one_box(xyxy2, img_init, label=label, color=colors(c, True), line_thickness=line_thickness)
            print(f'{s}Done. ({t2 - t1:.3f}s)')
            # cv2.imshow(str(p), im0)
            cv2.imshow(str(p), img_init)
            while True:
                user_input = cv2.waitKey(3000)
                if user_input == ord('q'):
                    break
            cv2.destroyAllWindows()
