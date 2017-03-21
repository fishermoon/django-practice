from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})
