from datetime import timedelta

from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rental
from books.models import Book
from books.serializers import BookSerializer