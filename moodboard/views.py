from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def home(request):
    posts = {
        'posts': Post.objects.all()
    }
    return render(request, 'moodboard/home.html',posts)

class PostView(ListView):
    model = Post

    # <app>/<model>_<viewtype>.html
    template_name = 'moodboard/home.html'
    context_object_name = 'posts'

    # Change order
    ordering = ['-published_date']


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post

    # Establish form fields
    fields = ['title', 'text']


    # Override form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    # Establish form fields
    fields = ['title', 'text']


    # Override form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class  DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'moodboard/about/')

    
# References 

# https://ccbv.co.uk/