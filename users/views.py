from django.shortcuts import render, redirect

from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # Form validation
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            # redirect user back to home page
            return redirect('login')
        
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:

        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

