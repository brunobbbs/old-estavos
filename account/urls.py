from django.conf.urls import patterns, url

# from django.contrib.auth import views as auth_views
from account import views as auser_views

urlpatterns = \
    patterns('',
             url(r'^login/$', auser_views.login, {'template_name': 'account/login.html'}, name='auth_login'),
             url(r'^logout/$', auser_views.logout, name='auth_logout'),
             url(r'^manage/$', auser_views.manage, name='auth_manage'),
             url(r'^profile/$', auser_views.profile,
                 {'template_name': 'account/profile.html'}, name='auth_profile'),
             url(r'^register/$', auser_views.register,
                 {'template_name': 'account/register.html'}, name="auth_register"),
             url(r'^register/successful/$', auser_views.registration_successful,
                 {"template_name": "account/registration_successful.html"}, name="registration_successful"),
             # url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),  # not implemented
             # url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),  # not implemented
             # url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),  # not_implemented
             # url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),  # not implemented
             # url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),  # not implemented
             # url(r'^password/reset/done/$', auth_views.password_reset_done,
             # name='auth_password_reset_done'),  # not implemented
             )
