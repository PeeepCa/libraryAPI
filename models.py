# DB model init

from datetime import datetime
from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    loans = db.relationship('Loan', backref='book', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'is_available': self.is_available
        }


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'user_id': self.user_id,
            'loan_date': self.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else None
        }
