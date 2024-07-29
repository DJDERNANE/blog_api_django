from django.shortcuts import render
from post.models import Article, Comment
from post.serializer import ArticleSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q 
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request) :
    data = request.data
    username = request.user
    try:
        user = User.objects.get(username=username)  # Fetch the full User object
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ArticleSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(user=user)  # Automatically set the user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit(request, pk) :
    data = request.data
    username = request.user
    try:
        user = User.objects.get(username=username)  # Fetch the full User object
    except User.DoesNotExist:
        return Response({'detail': 'User not not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        article = Article.objects.get(id=pk)  # Fetch the full User object
    except User.DoesNotExist:
        return Response({'detail': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ArticleSerializer(article, data=data)
    
    if serializer.is_valid():
        serializer.save(user=user)  # Automatically set the user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myarticles(request) :
    username = request.user
    try:
        user = User.objects.get(username=username)  # Fetch the full User object
    except User.DoesNotExist:
        return Response({'detail': 'User not not found'}, status=status.HTTP_404_NOT_FOUND)
    
    articles = Article.objects.filter(user=user)  # Use filter to get all articles for the user
    serializer = ArticleSerializer(articles, many=True)  # Serialize the list of articles
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def articles(request) :
    articles = Article.objects.all().order_by('-published_date')  # Use filter to get all articles for the user
    serializer = ArticleSerializer(articles, many=True)  # Serialize the list of articles
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def show(request,pk) :
    try :
        articles = Article.objects.get(id=pk)  # Use filter to get all articles for the user
        serializer = ArticleSerializer(articles, many=False)  # Serialize the list of articles
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Article.DoesNotExist :
        raise NotFound('Article not found')
    
@api_view(['DELETE'])
def delete(request,pk) :
    try :
        article = Article.objects.get(id=pk)  # Use filter to get all articles for the user
        article.delete()
        return Response({'details ' : 'article deleted'}, status=status.HTTP_200_OK)
    except Article.DoesNotExist :
        raise NotFound('Article not found')

@api_view(['POST'])    
@permission_classes([IsAuthenticated])
def comment(request, Aid):
    try:
        article = Article.objects.get(id=Aid)
        user = User.objects.get(username=request.user)
        if request.data['parent']:
            parent = Comment.objects.get(id=request.data['parent'])
        else:
            parent = None
        comment = Comment.objects.create(user=user, article=article, content=request.data['content'], parent_comment=parent)
        commentSerializer = CommentSerializer(comment)
        return Response(commentSerializer.data, status.HTTP_201_CREATED)
    except Article.DoesNotExist:
        return Response({'detail': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])    
def articleComments(request, Aid):
    try:
        article = Article.objects.get(id=Aid)
        comments = Comment.objects.filter(article=article)
        commentsSerializer = CommentSerializer(comments, many=True)
        return Response(commentsSerializer.data, status.HTTP_200_OK)
    except Article.DoesNotExist:
        return Response({'detail': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])    
def commentReplies(request, Cid):
    try:
        comment = Comment.objects.get(id=Cid)
        replies = Comment.objects.filter(parent_comment=comment)
        commentsSerializer = CommentSerializer(replies, many=True)
        return Response(commentsSerializer.data, status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({'detail': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    
       