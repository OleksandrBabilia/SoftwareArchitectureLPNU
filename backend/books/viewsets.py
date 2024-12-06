from datetime import timezone, datetime, timedelta

from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsStuffUserOrReadOnly
from .models import Book, Ganre
from .serializers import BookSerializer, GanreSerializer
from rentals.models import Rental


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    @permission_classes((IsAuthenticatedOrReadOnly,))  # Apply specific permission
    def rent(self, request, pk=None):
        """Endpoint for renting a book with a specified rental date."""
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication is required to rent a book."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        book = self.get_object()
        user = request.user
        # Check if the book is already rented
        if Rental.objects.filter(book=book, is_returned=False).exists():
            return Response(
                {"error": "Book is already rented by someone else."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get rental_date from request

        rental_date_str = request.data.get('rental_date')
        return_date_str = request.data.get('return_date')

        # Default return date if not provided
        default_return_date = datetime.now() + timedelta(days=7)

        if not rental_date_str:
            return Response(
                {"error": "Rental date is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parse rental_date and return_date
        rental_date = parse_datetime(rental_date_str)
        return_date = parse_datetime(return_date_str) if return_date_str else default_return_date

        if not rental_date:
            return Response(
                {"error": "Invalid rental date format. Use ISO 8601 (e.g., '2024-11-15T10:00:00Z')."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check return_date validity
        if return_date and return_date < rental_date:
            return Response(
                {"error": "Invalid return date. Return date must be after the rental date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a rental record
        rental = Rental.objects.create(user=user, book=book, rental_date=rental_date, return_date=return_date)
        rental.save()
        print(rental.return_date)

        # Mark the book as rented
        book.rented = True
        book.save()

        return Response({"success": f"Book '{book.title}' rented successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @permission_classes((IsAuthenticatedOrReadOnly,))  # Apply specific permission
    def return_book(self, request, pk=None):
        """Endpoint for returning a book."""
        book = self.get_object()
        user = request.user.id

        # Find the rental record
        rental = Rental.objects.filter(book=book, user=user, is_returned=False).first()
        if not rental:
            return Response(
                {"error": "You have not rented this book or it has already been returned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark as returned
        rental.is_returned = True
        rental.return_date = datetime.now()
        rental.save()

        # Mark the book as not rented
        book.rented = False
        book.save()

        return Response({"success": f"Book '{book.title}' returned successfully."}, status=status.HTTP_200_OK)


class GanreViewSet(viewsets.ModelViewSet):
    queryset = Ganre.objects.all()
    serializer_class = GanreSerializer
    permission_classes = [IsAuthenticated]
