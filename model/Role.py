from model.SerializableModel import SerializableModel, db


class Role(db.Model, SerializableModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
