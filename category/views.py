
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Categories
from .serializer import CategorySerializer
from django.db.models.query import QuerySet
import re

@api_view(['POST'])
def register_category(request):
    name = request.data.get('name')
    description = request.data.get('description')
    
    
    # Perform validation or any other logic you need
    if not all([name, description]):
        # Data PreProcessing & Santization
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    if not re.match(r'^[A-Za-z_]+$', name) or len(name) < 3 or len(name) > 50:
        return Response({"error": "Name must be between 3 and 50 characters and can only contain letters and underscores (_). No spaces, numbers, or special characters allowed."}, status=status.HTTP_400_BAD_REQUEST)
    if len(description) < 10 or len(description) > 500:
        return Response({"error": "Description must be between 10 and 500 characters."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Save the input to the UserProfile model
        category_created = Categories(name=name,description=description )
        category_created.save()
    
    # Example response data
    response_data = {
        "message": "Category registered successfully!",
        "categories": {
            "name": name,
            "description":description
        }
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        categories: QuerySet = Categories.objects.all()
        if not categories.exists():
            return Response({'message': 'No categories found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)
    

@api_view(['PATCH'])
def update_patch_api(request, pk):
    try:
        # Fetch the customer instance based on the primary key (id)
        categories = Categories.objects.get(pk=pk)
    except Categories.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    # Use partial=True to allow partial updates (only updating the 'name' field)
    serializer = CategorySerializer(categories, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_put_api(request):
    pk = request.data.get('id')
    if not pk:
        return Response({'error': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        categories = Categories.objects.get(pk=pk)
    except Categories.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    # Deserialize the incoming data
    serializer = CategorySerializer(categories, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
    {
        "message": "Category updated!",
        "data": serializer.data
    },
    status=status.HTTP_200_OK
)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['DELETE'])
def delete_api(request):
    pk = request.data.get('id')
    if not pk:
        return Response({'error': 'ID not provided'}, status=400)
    try:
        categories = Categories.objects.get(pk=pk)
        categories.delete()
        return Response({'message': 'Category deleted successfully'}, status=200)
    except Categories.DoesNotExist:
        return Response({'error': 'Category not found'}, status=400)

