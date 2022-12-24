class VisualElement:
    def __init__(self, point, element_type, text=None, border=None):
        self.location = Point(point[0], point[1])
        self.element_type = element_type
        self.text = text
        self.border = border


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
