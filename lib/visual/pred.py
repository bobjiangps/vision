import torch
import requests
from lib.visual.experiment import load
from lib.visual.datasets import LoadImages
from lib.visual.common import check_img_size, non_max_suppression, scale_coords
from lib.visual.torch_assistant import time_synchronized
from conf.config import LoadConfig
from pathlib import Path


def init_model(project="Blog", name=None, remove=False, state=False, device=torch.device("cpu")):
    suffix = "pth" if state else "pt"
    if name:
        model = f"{name}.{suffix}"
    else:
        model = f"{LoadConfig().model['weights']}.{suffix}"
    Path.cwd().joinpath("resource", "models").mkdir(parents=True, exist_ok=True)
    Path.cwd().joinpath("resource", "img").mkdir(parents=True, exist_ok=True)
    path = Path.cwd().joinpath("resource", "models", model)
    if remove:
        path.unlink()
    if not path.exists():
        print("model not exist, start download...")
        r = requests.get(f"{LoadConfig().remote}/{project}/{model}")
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            print("download complete...")
        else:
            print(f"download failed with status code: {r.status_code}")
    else:
        print("model exist")
    return load(path, map_location=device)


def predict(model, device=torch.device("cpu")):
    config = LoadConfig().model
    stride = int(model.stride.max())
    imgsz = check_img_size(640, s=stride)
    names = model.module.names if hasattr(model, 'module') else model.names
    dataset = LoadImages(Path.cwd().joinpath("resource", "img", f"{config['img']}.png"), img_size=imgsz, stride=stride)
    label_store = {}
    results = []
    shape = None
    for path, img, im0s in dataset:
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
            # shape = im0.shape
            pad = LoadConfig().model["pad"]
            shape = (im0.shape[0], im0.shape[1] + pad * 2, im0.shape[2])
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    if label_store.get(names[c]):
                        label_store[names[c]] += 1
                    else:
                        label_store[names[c]] = 1
                    results.append({"N": names[c], "PR": f"{conf:.2f}", "COOR": (int(xyxy[0])+pad, int(xyxy[1]), int(xyxy[2])+pad, int(xyxy[3]))})
            print(f'{s}Predict Done. ({t2 - t1:.3f}s)')
    return results, label_store, shape
