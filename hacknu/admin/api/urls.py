from django.urls import path
from .views import ListUsersView, UserCreateView
from .views import ListBooksView, BookCreateView
from .views import book_list


urlpatterns = [
    path('users/', ListUsersView.as_view(), name="users-all"),
    path('users/create/', UserCreateView.as_view(), name="user-create"),
    path('books/', ListBooksView.as_view(), name="books-all"),
    path('books/create/', BookCreateView.as_view(), name="book-create"),
    path('', book_list, name='post_list'),
]