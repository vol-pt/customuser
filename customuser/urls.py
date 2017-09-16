from django.conf.urls import url
from django.contrib import admin
from emailuser.views import register, EmailUserLogin, ProfileView, CustomLogoutView, UserListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', register, name='register'),
    url(r'^login/$', EmailUserLogin.as_view(), name='login'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='accounts_profile'),
    url(r'^logout/$', CustomLogoutView.as_view()),
    url(r'^users/$', UserListView.as_view())
]
