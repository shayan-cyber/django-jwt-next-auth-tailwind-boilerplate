from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from . serializers import (
    UserSerializer
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

@api_view(['GET'])
def heart_beat(request):
    return Response({"message":"hello"},status = status.HTTP_200_OK)




@api_view(["POST"])
def signin(request):
    data = request.data
    user_obj = User.objects.filter(username = data['username'])
    if user_obj:
        user = authenticate(username = data['username'], password = data['password'])
        if user is None:
            return Response({"message":"Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            refresh = RefreshToken.for_user(user)

            return Response({"username":user.get_username(), 'refresh': str(refresh),'access': str(refresh.access_token)}, status= status.HTTP_202_ACCEPTED)
    else:
        if not 'first_name' in data:
            data['first_name'] = data['username']
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        
            user_obj = get_object_or_404(User, id = serializer.data['id'])
            refresh = RefreshToken.for_user(user_obj)

            return Response({"serializer-data":serializer.data, "username":user_obj.username, 'refresh': str(refresh),'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            





@api_view(['POST'])
def register(request):
    data = request.data
    if not data['first_name']:
        data['first_name'] = data['username']
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
       
        user_obj = get_object_or_404(User, id = serializer.data['id'])
    

        return Response({"serializer-data":serializer.data, "username":user_obj.username}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)