# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from sampleapp.tokens import account_activation_token
from website.settings import EMAIL_HOST_USER
from .forms import SignUpForm

# Create your views here.

def index_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sampleapp:home'))

    template = 'sampleapp/index.html'

    context = {}
    kwargs = request.session
    if kwargs:
        if 'signup_form' in kwargs:
            signUpForm = kwargs.get('signup_form')
            kwargs.pop('signup_form', None)
        else:
            signUpForm = SignUpForm()

        if 'signin_error' in kwargs:
            context['signin_error'] = kwargs.get('signin_error')
            kwargs.pop('signin_error', None)

        if 'signin_username' in kwargs:
            context['signin_username'] = kwargs.get('signin_username')
            kwargs.pop('signin_username', None)

        if 'redirect_from' in kwargs:
            context['redirect_from'] = kwargs.get('redirect_from')
            kwargs.pop('redirect_from', None)
    else:
        signUpForm = SignUpForm()
    context['signup_form'] = signUpForm
    return render(request, template, context)


def signup_view(request):
    '''
    Sign up functionality.
    :param request:
    :return:
    '''

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            subject = 'Welcome to Ting! Thanks for signing up!'

            message = render_to_string('sampleapp/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)

            print (send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[user.email,], fail_silently=False))
            return HttpResponseRedirect(reverse('sampleapp:account_activation_sent'))
        else:
            request.session['signup_form'] = form
            request.session['redirect_from'] = 'signup'
            return HttpResponseRedirect(reverse('sampleapp:index'))

    return HttpResponseRedirect(reverse('sampleapp:index'))


def login_view(request):
    if request.method == 'POST':
        # Correct login method.
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(username=uname, password=pwd)

        if user is not None:
            # The redirect must be to the home page. Change this later.
            login(request, user)
            return HttpResponseRedirect(reverse('sampleapp:home'))
        else:
            # Mark the error and send it back. We're clearing out the password and keeping the username.
            request.session['signin_error'] = 'Incorrect username or password.'
            request.session['signin_username'] = uname
            request.session['redirect_from'] = 'login'
            return HttpResponseRedirect(reverse('sampleapp:index'))
    else:
        # Incorrect method of login. Might need to change this later.
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('sampleapp:index'))

        return HttpResponseRedirect(reverse('sampleapp:home'))


def about_view(request):
    return render(request, 'sampleapp/about.html')


@login_required(login_url='/music/login/')
def home_view(request):
    form = PasswordChangeForm(user=request.user)
    context = {'change_pwd_form': form}
    return render(request, 'sampleapp/home.html', context)


@login_required(login_url='/music/login')
def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sampleapp:login'))
    return render(request, 'sampleapp/profile.html', {'user': request.user})


@login_required(login_url='/music/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('sampleapp:index'))


@login_required(login_url='/music/login')
def change_pwd(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('sampleapp:index'))
        else:
            return render(request, "sampleapp/change_pwd.html", { 'change_pwd_form': form })
    else:
        return HttpResponseRedirect(reverse('sampleapp:home'))


def account_activation_sent(request):
    return render(request, 'sampleapp/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('sampleapp:index'))
    else:
        return render(request, 'sampleapp/account_activation_invalid.html')


'''
Not used.
class SignUpView(View):
    def get(self, request):
        return render(request, 'sampleapp/signup.html')

    def post(self, request):
        uname = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        newuser = User.objects.create_user(username=uname,
                                           email=email,
                                           password=pwd,
                                           first_name=fname,
                                           last_name=lname)
        newuser.save()

        return redirect('/music/')
        
        
class SignInView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'sampleapp/signin.html')

        

    def post(self, request):
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(username=uname, password=pwd)

        if user is not None:
            # Change this.
            return HttpResponseRedirect(reverse('sampleapp:profile', args=(user.get_username(),)))
        else:
            context = {'error': 'Username %s does not exist.' % uname}
            return render(request, 'sampleapp/signin.html', context)
            
        
class IndexView(TemplateView):
    template_name = 'sampleapp/index.html'

    def get_context_data(self, **kwargs):
        context = TemplateView().get_context_data(**kwargs)
        if self.request.user:
            context['user'] = self.request.user
        return context
'''