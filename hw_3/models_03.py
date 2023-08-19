from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    group = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    ratings = db.relationship('Rating', backref='student', lazy=True)

    def __repr__(self):
        return f'Student({self.name}, {self.surname}, {self.group}, {self.email})'


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    sub_study = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Rating({self.student_id}, {self.sub_study}, {self.rating})'
