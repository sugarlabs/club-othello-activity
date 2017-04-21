class IOObject:
    def __init__(self, engine=""):
        self.__id = 0
        self.engine = engine

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def new_event(self, event):
        pass

    def set_engine(self, engine):
        self.engine = engine