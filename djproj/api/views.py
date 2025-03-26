from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from post.models import Post
from comments.models import Comment
from .serializers import PostSerializer, CommentSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets


# Create your views here.


def api_test(request):
    posts = Post.objects.all()
    posts_data = list(posts.values())
    return JsonResponse(posts_data, safe=False)


@api_view(['GET', 'POST'])
def get_post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serialized_data = PostSerializer(posts, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serialized_data = PostSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Same as above def method but as a class method
# class PostsAPI(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serialized_data = PostSerializer(posts, many=True)
#         return Response(serialized_data.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serialized_data = PostSerializer(data=request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(serialized_data.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

# Same as above class method but with mixins plugins
class PostsAPI(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
# Same as above class method but with Generic
# class PostsAPI(generics.ListAPIView, generics.CreateAPIView):
class PostsAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['GET', 'PUT'])
def get_post_detail(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serialized_data = PostSerializer(post)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serialized_data = PostSerializer(post, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Same as above def method but as a class method
# class PostDetailAPI(APIView):
#     def _get_object(self, pk):
#         try:
#             post = Post.objects.get(id=pk)
#             return post
#         except Post.DoesNotExist:
#             return Http404
        
#     def get(self, request, pk):
#         post_data = self._get_object(pk)
#         serialized_data = CommentSerializer(post_data)
#         return Response(serialized_data.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         post_data = self._get_object(pk)
#         serialized_data = CommentSerializer(post_data, data=request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(serialized_data.data, status=status.HTTP_200_OK)
#         return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         post_data = self._get_object(pk)
#         post_data.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # Same as above class method but with mixins plugins
# class PostDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, pk):
#         return self.retrieve(request, pk)
    
#     def put(self, request, pk):
#         return self.update(request, pk)
    
#     def delete(self, request, pk):
#         return self.destroy(request, pk)


# Same as above class method but with Generic
# class PostDetailAPI(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'

# ViewSet
# class PostsAPIViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Post.objects.all()
#         serialized_data = PostSerializer(queryset, many=True)
#         return Response(serialized_data.data)
    
#     def create(self, request):
#         serialized_data = PostSerializer(data=request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(serialized_data.data, status=status.HTTP_200_OK)
#         return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def retrieve(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         serialized_data = PostSerializer(post)
#         return Response(serialized_data.data, status=status.HTTP_200_OK)
        
#     def update(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         serialized_data = PostSerializer(post, data=request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(serialized_data.data, status=status.HTTP_200_OK)
#         return Response(serialized_data.errors)
    
#     def delete(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# Same as the above class but less code because of ModelViewSet
class PostsAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCommentsAPI(APIView):
    def get(self, request, pk):
        comments = Comment.objects.filter(comment_post=pk)
        serialized_data = CommentSerializer(comments, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serialized_data = CommentSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        

class PostCommentsAPIViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
