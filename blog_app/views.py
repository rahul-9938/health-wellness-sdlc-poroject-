import os
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Blog
from .serializer import BlogSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser



@api_view(['POST'])
def create_blog(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET'])
def list_blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def retrieve_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)


@api_view(['PUT'])
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def partial_update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    serializer = BlogSerializer(blog, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_blog_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    title = request.data.get('title')
    content = request.data.get('content')
    category_id = request.data.get('category')
    tags = request.data.getlist('tags')
    image_file = request.FILES['image']
    
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'blog_images')

    file_path = os.path.join(upload_dir, image_file.name)

    with open(file_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    blog = Blog.objects.create(
        title=title,
        content=content,
        category_id=category_id,
        tags=tags,
        filename=image_file.name  
    )

    image_url = request.build_absolute_uri(settings.MEDIA_URL + 'blog_images/' + image_file.name)

    return Response({
        'message': 'Blog created successfully!',
        'blog': {
            'title': blog.title,
            'filename': blog.filename,
            'image_url': image_url
        }
    }, status=status.HTTP_201_CREATED)
