import pytest
from rest_framework import status
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from authors.models import Author
from publishers.models import Publisher
from rentals.models import Rental
from books.models import Book, Ganre

@pytest.fixture
def user():
    """Fixture for creating a user."""
    user = User.objects.create_user(username='testuser', password='password')
    return user

@pytest.fixture
def author():
    """Fixture for creating an author."""
    return Author.objects.create(name="Test Author")

@pytest.fixture
def publisher():
    """Fixture for creating a publisher."""
    return Publisher.objects.create(name="Test Publisher")

@pytest.fixture
def ganre():
    """Fixture for creating a ganre."""
    return Ganre.objects.create(name="Fantasy")

@pytest.fixture
def book(author, publisher, ganre):
    """Fixture for creating a book."""
    book = Book.objects.create(
        title="Test Book",
        isbn="1234567890123",
        publication_date=datetime.now(),
        price=19.99,
        author=author,
        publisher=publisher,
        page_count=200,
        rating=4.5
    )
    book.ganres.add(ganre)
    return book

@pytest.fixture
def api_client():
    """Fixture for setting up an API client."""
    return APIClient()

# Test the book rent functionality
@pytest.mark.django_db
def test_rent_book(api_client, user, book):
    api_client.force_authenticate(user=user)
    rental_date = make_aware(datetime.now())
    return_date = make_aware(datetime.now() + timedelta(days=7))

    response = api_client.post(
        f'/books/{book.id}/rent/',
        {'rental_date': rental_date.isoformat(), 'return_date': return_date.isoformat()}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "rented" in response.data['success']
    assert Rental.objects.filter(book=book, user=user).exists()
    book.refresh_from_db()
    assert book.rented is True

# Test trying to rent a book that's already rented
@pytest.mark.django_db
def test_rent_book_already_rented(api_client, user, book):
    # Create a rental first
    rental = Rental.objects.create(user=user, book=book, rental_date=make_aware(datetime.now()))
    book.rented = True
    book.save()

    api_client.force_authenticate(user=user)
    rental_date = make_aware(datetime.now())
    return_date = make_aware(datetime.now() + timedelta(days=7))

    response = api_client.post(
        f'/books/{book.id}/rent/',
        {'rental_date': rental_date.isoformat(), 'return_date': return_date.isoformat()}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Book is already rented" in response.data['error']

# Test the book return functionality
@pytest.mark.django_db
def test_return_book(api_client, user, book):
    # Rent a book first
    rental_date = make_aware(datetime.now())
    return_date = make_aware(datetime.now() + timedelta(days=7))
    rental = Rental.objects.create(user=user, book=book, rental_date=rental_date, return_date=return_date)

    api_client.force_authenticate(user=user)

    response = api_client.post(f'/books/{book.id}/return_book/')
    assert response.status_code == status.HTTP_200_OK
    assert "returned" in response.data['success']
    rental.refresh_from_db()
    assert rental.is_returned is True

# Test attempting to return a book that was not rented
@pytest.mark.django_db
def test_return_book_not_rented(api_client, user, book):
    api_client.force_authenticate(user=user)

    response = api_client.post(f'/books/{book.id}/return_book/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "You have not rented this book" in response.data['error']

# Test renting a book without specifying a rental date
@pytest.mark.django_db
def test_rent_book_without_rental_date(api_client, user, book):
    api_client.force_authenticate(user=user)

    response = api_client.post(
        f'/books/{book.id}/rent/',
        {'return_date': (make_aware(datetime.now() + timedelta(days=7))).isoformat()}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Rental date is required" in response.data['error']

# Test renting a book with an invalid rental date format
@pytest.mark.django_db
def test_rent_book_invalid_rental_date_format(api_client, user, book):
    api_client.force_authenticate(user=user)

    response = api_client.post(
        f'/books/{book.id}/rent/',
        {'rental_date': 'invalid_date', 'return_date': (make_aware(datetime.now() + timedelta(days=7))).isoformat()}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid rental date format" in response.data['error']
