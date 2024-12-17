import abc
class BasicFunctions(abc.ABC):
    @abc.abstractmethod
    def create_user_interface (self) : pass

    @abc.abstractmethod
    def open_image(self): pass

    @abc.abstractmethod
    def save_file(self): pass

    @abc.abstractmethod
    def undo(self): pass

    @abc.abstractmethod
    def redo(self): pass

    @abc.abstractmethod
    def set_image_bg(self): pass

    @abc.abstractmethod
    def add_text(self): pass

    @abc.abstractmethod
    def add_line(self): pass

    @abc.abstractmethod
    def add_shape(self): pass
