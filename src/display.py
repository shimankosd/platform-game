from pygame.display import get_surface


class Display:
    """
    Allows to init display in subclasses
    """
    def __init__(self):
        self._display = None

    def display_init(self):
        self._display = get_surface()
