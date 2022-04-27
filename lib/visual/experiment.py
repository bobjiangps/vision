import torch
import torch.nn as nn
from conf.config import LoadConfig


class Ensemble(nn.ModuleList):
    def __init__(self):
        super(Ensemble, self).__init__()

    def forward(self, x, augment=False, profile=False, visualize=False):
        y = []
        for module in self:
            y.append(module(x, augment, profile, visualize)[0])
        y = torch.cat(y, 1)
        return y, None


def load(weights, map_location=None):
    model = Ensemble()
    if str(weights).endswith(".pt"):
        ckpt = torch.load(weights, map_location=map_location)
        model.append(ckpt['ema' if ckpt.get('ema') else 'model'].float().fuse().eval())
    else:
        from lib.visual.model import Model
        # ckpt = Model("yolov5s.yaml", 3, 6, None).to("cpu")
        ckpt = Model(LoadConfig().model, 3, 6, None).to("cpu")
        ckpt.load_state_dict(torch.load(weights, map_location=map_location))
        ckpt.eval()
        ckpt.names = LoadConfig().model["n"]
        model.append(ckpt)

    if len(model) == 1:
        return model[-1]
    else:
        print(f'Ensemble created with {weights}\n')
        for k in ['names']:
            setattr(model, k, getattr(model[-1], k))
        model.stride = model[torch.argmax(torch.tensor([m.stride.max() for m in model])).int()].stride
        return model
