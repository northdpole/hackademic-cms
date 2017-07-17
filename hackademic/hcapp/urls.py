from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
app_name = 'hcapp'

urlpatterns = [
    #/hcapp/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /hcapp/articles/
    url(r'^users$', views.UserView.as_view(), name='users'),
    # /hcapp/users/$(users.slug)
    url(r'^users/(?P<slug>[-\w]+)/$', views.UserDetail.as_view(), name='users-details'),
    #/hcapp/register/
    url(r'^register$', views.UserCreation.as_view(), name='register'),
    # /hcapp/login/
    url(r'^login$', views.LoginView.as_view(), name='login'),
    # /hcapp/logout/
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    #/hcapp/articles/
    url(r'^articles$', views.ArticleView.as_view(), name='articles'),
    # /hcapp/articles/create
    url(r'^articles/create$', views.ArticleCreation.as_view(), name='articles-create'),
    #hcapp/articles/$(article.slug)
    url(r'^articles/(?P<slug>[-\w]+)/$', views.ArticleDetail.as_view(), name='article-details'),
    # /hcapp/challenges/
    url(r'^challenges$', views.ChallengeView.as_view(), name='challenges'),
    # /hcapp/challenges/create
    url(r'^challenges/create$', views.ChallengeCreation.as_view(), name='challenge-create'),
    # hcapp/challenges/$(challenge.slug)
    url(r'^challenges/(?P<slug>[-\w]+)/$', views.ChallengeDetail.as_view(), name='challenge-details'),
    # hcapp/menu-manager
    url(r'^menu-manager/$', views.MenuView.as_view(), name='menu-manager'),
    # hcapp/options
    url(r'^options/$', views.OptionsView.as_view(), name='options'),
]