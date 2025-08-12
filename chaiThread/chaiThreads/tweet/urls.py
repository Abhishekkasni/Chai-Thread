from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('save/<int:tweet_id>/', views.save_tweet, name='save_tweet'),
    path('saved/', views.saved_tweets, name='saved_tweets'),
    path('tweet/<int:tweet_id>/unsave/', views.unsave_tweet, name='tweet_unsave'),
    path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),  # ✅ Added!
    path('comment/<int:comment_id>/delete/',views.delete_comment,name='delete_comment'),
    path('accounts/emailsignup', views.register, name='register'),
    path('<str:username>/', views.profile_view, name='profile'),
    path('<int:tweet_id>/repost/', views.tweet_repost, name='tweet_repost'),
]
