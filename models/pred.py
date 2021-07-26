import torch
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.torch_utils import time_synchronized
from conf.config import LoadConfig
from pathlib import Path


def init_model(device=torch.device("cpu")):
    config = LoadConfig().model
    model = attempt_load(Path.cwd().joinpath("resource", "models", f"{config['weights']}.pt"), map_location=device)
    return model


def predict(model, device=torch.device("cpu")):
    config = LoadConfig().model
    stride = int(model.stride.max())
    imgsz = check_img_size(640, s=stride)
    names = model.module.names if hasattr(model, 'module') else model.names
    dataset = LoadImages(Path.cwd().joinpath("resource", "img", f"{config['img']}.png"), img_size=imgsz, stride=stride)
    label_store = {}
    results = []
    shape = None
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        t1 = time_synchronized()
        pred = model(img, augment=False, visualize=False)[0]
        pred = non_max_suppression(pred, config["confidence"], config["iou"], config["classes"], config["agnostic_nms"], max_det=config["max_det"])
        t2 = time_synchronized()
        for i, det in enumerate(pred):
            p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)
            shape = im0.shape
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    if label_store.get(names[c]):
                        label_store[names[c]] += 1
                    else:
                        label_store[names[c]] = 1
                    results.append({"N": names[c], "PR": f"{conf:.2f}", "COOR": (int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]))})
            print(f'{s}Done. ({t2 - t1:.3f}s)')
    return results, label_store, shape
