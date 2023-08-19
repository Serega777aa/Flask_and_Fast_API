from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    date_birth = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Student({self.name}, {self.email}, {self.password}, {self.date_birth})'

