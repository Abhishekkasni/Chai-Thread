from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Tweet, Comment
from .forms import TweetForm, UserRegistrationForm, CommentForm

def get_next_url(request, fallback='tweet_list'):
    return request.GET.get('next') or request.POST.get('next') or reverse(fallback)

def index(request):
    return render(request, 'index.html')
@login_required(login_url='/accounts/login/')
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    next_url = get_next_url(request)
    form = TweetForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        tweet = form.save(commit=False)
        tweet.user = request.user
        tweet.save()
        return redirect(next_url)
    return render(request, 'tweet_form.html', {'form': form, 'next': next_url})

@login_required
def tweet_edit(request, tweet_id):
    next_url = get_next_url(request)
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    form = TweetForm(request.POST or None, request.FILES or None, instance=tweet)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(next_url)
    return render(request, 'tweet_form.html', {'form': form, 'next': next_url})

@login_required
def tweet_delete(request, tweet_id):
    next_url = get_next_url(request)
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect(next_url)
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet, 'next': next_url})

@login_required
def save_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    tweet.saved_by.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unsave_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    request.user.saved_tweets.remove(tweet)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def saved_tweets(request):
    tweets = request.user.saved_tweets.all().order_by('-created_at')
    return render(request, 'saved_tweets.html', {'tweets': tweets})

@login_required
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    top_comments = tweet.comments.filter(parent__isnull=True).order_by('-created_at')
    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        parent_id = request.POST.get('parent_id')
        parent_obj = Comment.objects.filter(id=parent_id).first() if parent_id else None

        new_comment = form.save(commit=False)
        new_comment.tweet = tweet
        new_comment.author = request.user
        new_comment.parent = parent_obj
        new_comment.save()
        return redirect('tweet_detail', tweet_id=tweet.id)

    return render(request, 'tweet_detail.html', {
        'tweet': tweet,
        'top_comments': top_comments,
        'form': form
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    tweet_id = comment.tweet.id
    if request.method == 'POST':
        comment.delete()
        return redirect('tweet_detail', tweet_id=tweet_id)
    return render(request, 'comment_confirm_delete.html', {'comment': comment})


@login_required
def tweet_repost(request, tweet_id):
    original = get_object_or_404(Tweet, id=tweet_id)
    next_url = get_next_url(request)
    form = TweetForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        repost = form.save(commit=False)
        repost.user = request.user
        repost.original_tweet = original
        repost.save()
        return redirect(next_url)

    return render(request, 'tweet_repost_form.html', {
        'form': form,
        'original': original,
        'next': next_url
    })

def register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request, user)
        return redirect('tweet_list')
    return render(request, 'registration/register.html', {'form': form})

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=profile_user).order_by('-created_at')
    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'tweets': tweets
    })

