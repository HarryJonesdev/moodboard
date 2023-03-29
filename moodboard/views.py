from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


# Handle home page


post = [
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'Harry',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    },
    {
        'author': 'John',
        'title': 'Title',
        'content': ' Post content',
        'date_posted': '27/03/23'
    }

]
def home(request):
    context = {
        'posts': Post.objects.all()
        
    }
    return render(request, 'moodboard/home.html',context)

def about(request):
    return render(request, 'moodboard/about/')
    
