from rest_framework import generics
from .models import Users
from .serializers import UsersSerializer
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from django.db import IntegrityError


#class ListUsersView(APIView):
  #  """
   # #Provides a get method handler.
    #"""
#    queryset = Users.objects.all()
 #   serializer_class = UsersSerializer



class ListUsersView(APIView):
    def get(self, request, version):
        users = Users.objects.all()
        
        serializer = UsersSerializer(users, many=True)
        return Response({"users": serializer.data})
    
class UserCreateView(APIView):
    def post(self, request, version):
        """ telegram_id = request.data.get('telegram_id')
        telegram_id = request.data.get('is_bot')
        telegram_id = request.data.get('first_name')
        telegram_id = request.data.get('last_name')
        telegram_id = request.data.get('lan_code') """

        # Create an article from the above data
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_created = serializer.save()
                return Response({"success": "User '{}' created successfully".format(user_created.telegram_id)}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)

