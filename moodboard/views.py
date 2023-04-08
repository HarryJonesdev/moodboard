from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.shortcuts import render, redirect
import pickle
from django.utils import timezone
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


from django.shortcuts import get_object_or_404

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        response = super().form_valid(form)

        # Get the primary key of the created post
        post_pk = self.object.pk

        # Analyze the sentiment of the created post
        sentiment = analyze_sentiment(post_pk)

        # Update the sentiment of the created post
        post = Post.objects.get(pk=post_pk)
        post.sentiment = sentiment
        post.save()

        return response




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

# Load the pickled sentiment analysis model and vectorizer
with open('C:\\Users\\harry\\Desktop\\final_year_project\\moodboard\\sentiment_analysis_files\\Sentiment-LR.pickle', 'rb') as f:
    model = pickle.load(f)

with open('C:\\Users\\harry\\Desktop\\final_year_project\\moodboard\\sentiment_analysis_files\\vectorizer-ngram-(1,2).pickle', 'rb') as f:
    vectorizer = pickle.load(f)

def analyze_sentiment(post_pk):
    # Retrieve the post text from the Post model instance
    post = Post.objects.get(pk=post_pk)
    post_text = post.text

    # Preprocess the post text using the same transformations as were used during training
    # (Note: you may want to move these preprocessing steps into a separate function)
    post_text = post_text.lower()  # Convert to lowercase
    post_text = post_text.replace('\n', ' ')  # Remove line breaks
    post_text = post_text.replace('\r', ' ')
    post_text = post_text.replace('\t', ' ')
    post_text = post_text.strip()  # Remove leading/trailing whitespace

    # Use the vectorizer to transform the preprocessed post text into a numerical feature vector
    feature_vector = vectorizer.transform([post_text])

    # Feed the feature vector into the sentiment analysis model to obtain a predicted sentiment score
    predicted_sentiment = model.predict(feature_vector)[0]

    if predicted_sentiment == 1:
        return 'Positive'
    else:
        return 'Negative'

    
