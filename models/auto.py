from db import db

class AutoModel(db.Model):
    __tablename__ = 'autos'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    name = db.Column(db.String(80))
    color = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    user_id = db.Column(db.Integer)


    def __init__(self, year, name, color, price, user_id):
        self.year = year
        self.name = name
        self.color = color
        self.price = price
        self.user_id = user_id

    def json(self):
        return {'id': self.id, 'year': self.year, 'name': self.name, 'color': self.color, 'price': self.price, 'user_id': self.user_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
