from ..abstract.instruction import instruction


class CreateInterface_(instruction):
    def __init__(self, line, column, id_, attributes):
        super().__init__(line, column)
        self.id_ = id_
        self.attributes = attributes


    def Eject(self, env):
        pass
        