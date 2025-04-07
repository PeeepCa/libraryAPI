import requests
import pytest


# Base URL for the API
BASE_URL = "http://localhost:5000/api"
USER_ID = "42"

# Test data
TEST_BOOK = {
    "title": "Test Book",
    "author": "Test Author"
}


# Utility functions
def create_book():
    response = requests.post(f"{BASE_URL}/books", json=TEST_BOOK)
    assert response.status_code == 201
    return response.json()


def get_book(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200
    return response.json()


def borrow_book(book_id):
    headers = {"x-user-id": USER_ID}
    response = requests.post(f"{BASE_URL}/loans", headers=headers, json={"book_id": book_id})
    assert response.status_code == 201
    return response.json()


def return_book(book_id):
    headers = {"x-user-id": USER_ID}
    response = requests.put(f"{BASE_URL}/loans/{book_id}/return", headers=headers)
    assert response.status_code == 200
    return response.json()


# Test cases
class TestLibraryAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        # This runs before each test
        # You could add setup code here if needed
        yield
        # This runs after each test
        # You could add cleanup code here if needed

    def test_book_lifecycle(self):
        """Test the full lifecycle of a book: create, get, borrow, return"""
        # Create a new book
        new_book = create_book()
        book_id = new_book["id"]

        # Verify book was created correctly
        assert new_book["title"] == TEST_BOOK["title"]
        assert new_book["author"] == TEST_BOOK["author"]
        assert new_book["is_available"] == True

        # Get the book and verify details
        book = get_book(book_id)
        assert book["id"] == book_id
        assert book["title"] == TEST_BOOK["title"]

        # Borrow the book
        loan = borrow_book(book_id)
        assert loan["book_id"] == book_id
        assert loan["user_id"] == int(USER_ID)

        # Verify book is no longer available
        book = get_book(book_id)
        assert book["is_available"] == False

        # Return the book
        returned_loan = return_book(book_id)
        assert returned_loan["book_id"] == book_id
        assert returned_loan["return_date"] is not None

        # Verify book is available again
        book = get_book(book_id)
        assert book["is_available"] == True

    def test_get_all_books(self):
        """Test retrieving all books"""
        response = requests.get(f"{BASE_URL}/books")
        assert response.status_code == 200
        books = response.json()
        assert isinstance(books, list)

    def test_get_available_books(self):
        """Test retrieving available books"""
        response = requests.get(f"{BASE_URL}/books/available")
        assert response.status_code == 200
        books = response.json()
        assert isinstance(books, list)
        for book in books:
            assert book["is_available"] == True

    def test_user_loans(self):
        """Test retrieving user's loans"""
        headers = {"x-user-id": USER_ID}
        response = requests.get(f"{BASE_URL}/loans/user", headers=headers)
        assert response.status_code == 200
        loans = response.json()
        assert isinstance(loans, list)
        for loan in loans: assert loan["user_id"] == int(USER_ID)

    def test_borrow_unavailable_book(self):
        """Test borrowing an unavailable book should fail"""
        # Create and borrow a book
        new_book = create_book()
        book_id = new_book["id"]
        borrow_book(book_id)

        # Try to borrow it again with a different user
        headers = {"x-user-id": "43"}
        response = requests.post(
            f"{BASE_URL}/loans",
            headers=headers,
            json={"book_id": book_id}
        )
        assert response.status_code == 400

        # Clean up - return the book
        return_book(book_id)
