from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User

from rest_framework import routers
from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rest/', include(router.urls)),

    url(r'^login', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^projects', views.projects, name='projects'),
    url(r'^delete', views.delete, name='delete'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^', views.post_list, name='post_list'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
