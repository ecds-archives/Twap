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
    auth_form = AuthenticationForm(None, request.POST or None)
    msg = "Not Logged in"
    if auth_form.is_valid():
        login(request, auth_form.get_user())
        msg = 'Logged In'
        return HttpResponseRedirect(nextpage)
    return render(request, 'accounts/login.html', {
        'auth_form': auth_form,
        'title': 'User Login',
        'next': nextpage,
        'message': msg,
    })

def logout_user(request):
    logout(request)
    return render(request, 'accounts/logout.html', {})