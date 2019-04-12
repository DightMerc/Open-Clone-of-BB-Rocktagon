from .models import TelegramUser
from .models import Book

from .serializers import UsersSerializer
from .serializers import BookSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django.db import IntegrityError

from django.shortcuts import render


def book_list(request):
    books = Book.objects.all()
    return render(request, 'api/base.html', {'books':books})

class ListUsersView(APIView):
    def get(self, request, version):
        users = TelegramUser.objects.all()
        
        serializer = UsersSerializer(users, many=True)
        return Response({"users": serializer.data})
    
class UserCreateView(APIView):
    def post(self, request, version):

        # Create an article from the above data
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_created = serializer.save()
                return Response({"success": "User '{}' created successfully".format(user_created.telegram_id)}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)


            
class ListBooksView(APIView):
    def get(self, request, version):
        books = Book.objects.all()
        
        serializer = BookSerializer(books, many=True)
        return Response({"books": serializer.data})
    
class BookCreateView(APIView):
    def post(self, request, version):

        # Create an article from the above data
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_created = serializer.save()
                return Response({"success": "Book '{}' created successfully".format(user_created.title)}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


            


