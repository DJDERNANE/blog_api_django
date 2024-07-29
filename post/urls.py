from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.articles),
    path('article/comments/<str:Aid>', views.articleComments),
    path('article/my/', views.myarticles),
    path('article/create/', views.create),
    path('article/edit/<str:pk>', views.edit),
    path('article/delete/<str:pk>', views.delete),
    path('article/<str:pk>', views.show),
    path('comment/replies/<str:Cid>', views.commentReplies),
    path('comment/<str:Aid>', views.comment),
]   