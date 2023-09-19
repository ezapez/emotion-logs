from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.




def register(request):
    # make a new user
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        # process completed form
        form = UserCreationForm(data=request.POST)

    if form.is_valid():
        new_user = form.save()
        # log the user in and send to homepage
        login(request, new_user)
        return redirect('emotion_logs:index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)