import torch
import torch.nn as nn


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
    ckpt = torch.load(weights, map_location=map_location)
    model.append(ckpt['ema' if ckpt.get('ema') else 'model'].float().fuse().eval())
    if len(model) == 1:
        return model[-1]
    else:
        print(f'Ensemble created with {weights}\n')
        for k in ['names']:
            setattr(model, k, getattr(model[-1], k))
        model.stride = model[torch.argmax(torch.tensor([m.stride.max() for m in model])).int()].stride
        return model
