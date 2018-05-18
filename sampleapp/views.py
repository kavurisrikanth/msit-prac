# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import TemplateView

from sampleapp.tokens import account_activation_token
from website.settings import EMAIL_HOST_USER
from .forms import SignUpForm

# Create your views here.

# class IndexView(View):
#     def get(self, request):
#         return render(request, 'sampleapp/index.html')


def index_view(request):
    template = 'sampleapp/index.html'
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sampleapp:profile'))
    return render(request, template)


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

            print send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[user.email,], fail_silently=False)
            return HttpResponseRedirect(reverse('sampleapp:account_activation_sent'))
    else:
        form = SignUpForm()
    return render(request, 'sampleapp/signup.html', {'form': form})


def signin_view(request):
    print 'inside POST'
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(username=uname, password=pwd)
        login(request, user)

        if user is not None:
            return HttpResponseRedirect(reverse('sampleapp:profile'))
        else:
            context = {'error': 'Incorrect username or password.'}
            return render(request, 'sampleapp/signin.html', context)
    else:
        if not request.user.is_authenticated:
            return render(request, 'sampleapp/signin.html')

        return HttpResponseRedirect(reverse('sampleapp:profile'))


def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sampleapp:signin'))
    return render(request, 'sampleapp/profile.html', {'user': request.user})


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('sampleapp:index'))

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