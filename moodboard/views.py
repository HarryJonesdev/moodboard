from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Comment
from .forms import CommentForm
import requests
from django.shortcuts import render, redirect, reverse
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


# code references
# https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-editing/
# https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-display/



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

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
    

    # Calculate the overall sentiment of the comments on the post
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        comments = Comment.objects.filter(post=self.object)


        # Count the postive and negative comments
        pos =0
        neg =0
        comment_count = 0

        for comment in comments:
            comment_count +=1
            sentiment = comment.sentiment
            print(sentiment)
            if sentiment == 'Negative':
                neg+=1
            if sentiment == 'Positive':
                pos+=1
        
        print(pos)
        print(neg)


        # Percentage of postive comments
        if comment_count > 0:
            pos_percentage = (pos / comment_count) * 100
        
        else: 
            pos_percentage = 0
        
        print(pos_percentage)
        if pos_percentage >= 90:
            average_sentiment = 'Overwhemingly Positive'
        elif pos_percentage >= 70:
            average_sentiment = 'Positive'
        elif pos_percentage >= 50:
            average_sentiment = 'Mixed'
        elif pos_percentage >= 30:
            average_sentiment = 'Negative'
        else:
            average_sentiment = 'Overwhemingly negative'


        context['comments'] = comments
        context['post'] = self.object

        context['average_sentiment'] = average_sentiment

        
        



        return context



        
    

   

class PostsSearchView(ListView):
    model = Post
    template_name = 'moodboard/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Post.objects.filter(title__icontains=query).order_by('-published_date')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_queryset()

        pos = 0
        neg = 0
        post_count = 0

        for post in posts:
            post_count += 1
            sentiment = post.sentiment
            if sentiment == 'Negative':
                neg += 1
            if sentiment == 'Positive':
                pos += 1

        if post_count > 0:
            pos_percentage = (pos / post_count) * 100
        else:
            pos_percentage = 0

        if pos_percentage >= 90:
            average_sentiment = 'Overwhelmingly Positive'
        elif pos_percentage >= 70:
            average_sentiment = 'Positive'
        elif pos_percentage >= 50:
            average_sentiment = 'Mixed'
        elif pos_percentage >= 30:
            average_sentiment = 'Negative'
        else:
            average_sentiment = 'Overwhelmingly Negative'

        context['posts'] = posts
        context['average_sentiment'] = average_sentiment
        search_term = self.request.GET.get('q')
        context['average_sentiment_title'] = f"Overall Sentiment of Posts Containing '{search_term}'"

        return context




     
     
    
    
    


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

        post_text = form.cleaned_data['text']

        # Analyze the sentiment of the post text
        sentiment = analyze_sentiment(post_text)

        # Update the sentiment of the created post
        post = Post.objects.get(pk=post_pk)
        post.sentiment = sentiment
        post.save()

        return response


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = 'moodboard/add_comment.html'
    success_url = '/'


    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        response = super().form_valid(form)

       
        comment_pk = self.object.pk

       
        post_text = form.cleaned_data['text']

        # Analyze the sentiment of the post text
        sentiment = analyze_sentiment(post_text)

        
        comment = Comment.objects.get(pk=comment_pk)
        comment.sentiment = sentiment
        comment.save()

        return response
    
    def get_success_url(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post.get_absolute_url()

    




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

def analyze_sentiment(text):
 

    # Clean data
    text = text.lower()  
    text = text.replace('\n', ' ')  
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.strip()  

   # Vectorize
    feature_vector = vectorizer.transform([text])

   # Predict sentiment
    predicted_sentiment = model.predict(feature_vector)[0]

    if predicted_sentiment == 1:
        return 'Positive'
    else:
        return 'Negative'

