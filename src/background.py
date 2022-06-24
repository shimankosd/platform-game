from abc import ABC
from src.display import Display
from pygame.image import load
from pygame.transform import scale


class Layer(ABC):
    def __init__(self, pic_path: str, size: tuple, priority: int, coordinates=(0, 0), copying=True):
        self.pic_path = pic_path
        self.coordinates = coordinates
        self.size = size
        self.priority = priority
        self.copying = copying
        self.image = None

    def load_image(self):
        self.image = load(self.pic_path).convert_alpha()

    def scale_image(self):
        self.image = scale(self.image, self.size)


class StaticLayer(Layer):
    def __init__(self, pic_path: str, size: tuple, priority: int, coordinates=(0, 0), copying=True):
        super().__init__(pic_path, size, priority, coordinates, copying)


class DynamicLayer(StaticLayer):
    def __init__(self, pic_path: str, size: tuple, priority: int, speed: float, coordinates=(0, 0), copying=True):
        super().__init__(pic_path, size, priority, coordinates, copying)
        self.speed = speed


class Background(Display):
    """
    Parallax background consists of several layers. Each of them moves with different speed.
    Each layer follows some object. Coordinate on X-axis of this object must be defined 'object_pos_x' property.
    """
    def __init__(self, layers: list, copies: int, base_speed: float):
        super().__init__()
        self._layers = layers
        self._layers = sorted(self._layers, key=lambda layer: layer.priority)
        self.copies = copies
        self._base_speed = base_speed
        self._object_pos_x = 0
        self.screen_width = None

    def display_init(self):
        super().display_init()
        self.screen_width = self._display.get_width()
        for layer in self._layers:
            layer.load_image()
            layer.scale_image()

    @property
    def object_pos_x(self) -> int:
        """
        Tracked object actual X-axis coordinate
        """
        return self._object_pos_x

    @object_pos_x.setter
    def object_pos_x(self, value: int):
        """
        Defines point on X-axis of object that should be tracked
        :param value: object coordinate
        """
        if not isinstance(value, int):
            raise TypeError(f'Expected type float, got {type(value).__name__} instead')
        self._object_pos_x = value

    def show(self):
        """
        Draws background
        """
        for background_n in range(self.copies):
            speed = self._base_speed
            for layer in self._layers:
                if layer.copying and isinstance(layer, DynamicLayer):
                    x = self.screen_width * background_n - speed * self._object_pos_x
                    y = layer.coordinates[1]
                    self._display.blit(layer.image, (x, y))
                    speed += layer.speed
                else:
                    self._display.blit(layer.image, layer.coordinates)
