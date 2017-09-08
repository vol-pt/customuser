from django.conf.urls import url
from django.contrib import admin
from core.views import index, CustomLoginView, ProfileView, CustomLogoutView, UserListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^login/$', CustomLoginView.as_view()),
    url(r'^accounts/profile/$', ProfileView.as_view()),
    url(r'^logout/$', CustomLogoutView.as_view()),
    url(r'^users/$', UserListView.as_view())
]
