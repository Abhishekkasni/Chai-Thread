from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_list_or_404
# Create your views here.
def index(request):
    return render(request,'index.html')

def tweet_list(request):
    Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets': tweets})

def tweet_create(request):
    if request.method=='POST':
        form = TweetForm(request.POST, request.FILES)
    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})
