from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.utils.html import escape
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from rest_framework import viewsets

from .models import Post
from .serializers import UserSerializer, GroupSerializer
import logging
import json


# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

def login(request):
    data = {}
    logging.debug("request: " + request.method)
    if request.method == 'GET':
        #response = HttpResponse(escape(repr(request)))
        return render(request, 'blog/login.html', data)

    data['username'] = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=data['username'], password=password)
    if user is None:
        data['type'] = 'info'
        data['message'] = '다시 입력해 주세요.'
        return render(request, 'blog/login.html', data)

    # A backend authenticated the credentials
    logging.debug('username: ' + data['username'])
    logging.debug('password: ' + password)

    response = HttpResponse(escape(repr(request)))
    return render(request, 'blog/index.html', data)


def signup(request):
    data = {}
    if request.method == 'GET':
        return render(request, 'blog/signup.html', data)

    data['message'] = ''
    data['username'] = request.POST.get('username')
    data['email'] = request.POST.get('email')
    password = request.POST.get('password')
    confirm= request.POST.get('password_confirm')
    logging.debug(password);
    logging.debug(confirm);
    if password != confirm:
        data['message_type'] = 'error'
        data['message'] = '비밀번호가 일치하지 않습니다'
        return render(request, 'blog/signup.html', data)
    
    # check existed 
    if User.objects.filter(username=data['username']).exists():
        data['message_type'] = 'error'
        data['message'] = '이미 존재하는 아이디입니다.'
        return render(request, 'blog/signup.html', data)

    #signup
    user = User.objects.create_user(username=data['username'], email=data['email'], password=password)
    if user is None:
        data['message_type'] = 'error'
        data['message'] = '가입이 실패하였습니다.'
        return render(request, 'blog/signup.html', data)

    user = authenticate(username=data['username'], password=data['password'])
    login(request)
    return render(request, 'blog/login.html', data)

    
def projects(request):
    return render(request, 'blog/projects.html')


def delete(request):
    User.objects.all().delete()
    print("succeeded delete all users")
    return render(request, 'blog/index.html')

    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
