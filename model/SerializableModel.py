import app

db = app.db_config

class SerializableModel:
    def as_dict(self):
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # return {c: getattr(self, c) for c in self.__dict__.keys()}
        # print(isinstance(self, SerializableModel))
        if self.__mapper__:
            dictionary = {c: getattr(self, c) for c in self.__mapper__.attrs.keys()}
            convert_to_json = lambda v : v.as_dict() if isinstance(v, SerializableModel) else v
            dictionary = {c: convert_to_json(v) for c,v in dictionary.items()}
            return dictionary
        return None
