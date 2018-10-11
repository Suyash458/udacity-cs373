class Rectangle(object):
    def __init__(self, center, height, width, color):
        self.center = center
        self.height = height
        self.width = width
        self.color = color
    
    def get_center_x(self):
        return center[0]
    
    def get_center_y(self):
        return center[1]
    
    def get_points(self):
        center_x, center_y = self.center
        return [
            (center_x - self.width/2, center_y + self.height/2)
            (center_x + self.width/2, center_y + self.height/2),
            (center_x + self.width/2, center_y - self.height/2)
            (center_x - self.width/2, center_y - self.height/2)
        ]
