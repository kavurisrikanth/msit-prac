from django.conf.urls import url, include
# from views import (
#     IndexView,
#     SignInView,
#     signup_view,
#     SignUpView,
#     account_activation_sent,
#     activate
# )

from . import views

app_name = 'sampleapp'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^signin/$', views.signin_view, name='signin'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^about/$', views.about_view, name='about'),
    url(r'^home/$', views.home_view, name='home'),
    url(r'^change/$', views.change_pwd, name='change_pwd'),
]