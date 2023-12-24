from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from . serializers import (
    UserSerializer
)
# Create your views here.

@api_view(['GET'])
def heart_beat(request):
    return Response({"message":"hello"},status = status.HTTP_200_OK)




@api_view(['POST'])
def register(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
       
        user_obj = get_object_or_404(User, id = serializer.data['id'])
    

        return Response({"serializer-data":serializer.data, "username":user_obj.username}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)