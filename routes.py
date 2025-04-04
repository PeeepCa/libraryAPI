from flask import request, jsonify
from app import app, db
from models import Book, Loan
from datetime import datetime


# Book endpoints
@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())


@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or not 'title' in data or not 'author' in data:
        return jsonify({'error': 'Missing required fields'}), 400

    book = Book(
        title=data['title'],
        author=data['author'],
        is_available=data.get('is_available', True)
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201


@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    if 'title' in data: book.title = data['title']
    if 'author' in data: book.author = data['author']
    if 'is_available' in data: book.is_available = data['is_available']

    db.session.commit()
    return jsonify(book.to_dict())


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})


@app.route('/api/books/available', methods=['GET'])
def get_available_books():
    books = Book.query.filter_by(is_available=True).all()
    return jsonify([book.to_dict() for book in books])


# Loan endpoints
@app.route('/api/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return jsonify([loan.to_dict() for loan in loans])


@app.route('/api/loans/user', methods=['GET'])
def get_user_loans():
    user_id = request.headers.get('x-user-id')
    if not user_id: return jsonify({'error': 'User ID not provided in header'}), 400

    loans = Loan.query.filter_by(user_id=user_id).all()
    return jsonify([loan.to_dict() for loan in loans])


@app.route('/api/loans', methods=['POST'])
def create_loan():
    user_id = request.headers.get('x-user-id')
    if not user_id: return jsonify({'error': 'User ID not provided in header'}), 400

    data = request.get_json()
    if not data or not 'book_id' in data: return jsonify({'error': 'Missing book_id'}), 400

    book = Book.query.get_or_404(data['book_id'])
    if not book.is_available: return jsonify({'error': 'Book is not available'}), 400

    loan = Loan(
        book_id=book.id,
        user_id=user_id
    )
    book.is_available = False

    db.session.add(loan)
    db.session.commit()
    return jsonify(loan.to_dict()), 201


@app.route('/api/loans/<int:book_id>/return', methods=['PUT'])
def return_book(book_id):
    user_id = request.headers.get('x-user-id')
    if not user_id: return jsonify({'error': 'User ID not provided in header'}), 400

    # Find the active loan for this book and user
    loan = Loan.query.filter_by(
        book_id=book_id,
        user_id=user_id,
        return_date=None
    ).first_or_404()

    # Update loan and book status
    loan.return_date = datetime.now()
    book = Book.query.get(book_id)
    book.is_available = True

    db.session.commit()
    return jsonify(loan.to_dict())
