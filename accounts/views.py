from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

def authenticate_user(request):
    """Logs a user into the application."""
    nextpage = request.GET.get('next', reverse('twitter:summary'))
    if request.user.is_authenticated():
        return HttpResponseRedirect(nextpage)
    if request.method == 'POST':
        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return HttpResponseRedirect(nextpage)
    else:
        auth_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'auth_form': auth_form,
        'title': 'User Login',
        'next': nextpage,
    })

def logout_user(request):
    logout(request)
    return render(request, 'accounts/logout.html', {})