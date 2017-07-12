from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
app_name = 'hcapp'

urlpatterns = [
    #/hcapp/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /hcapp/articles/
    url(r'^users$', views.UserView.as_view(), name='users'),
    # /hcapp/users/$(users.id)
    url(r'^users/(?P<slug>\w+)/$', views.UserDetail.as_view(), name='users-details'),
    #/hcapp/register/
    url(r'^register$', views.UserCreation.as_view(), name='register'),
    # /hcapp/login/
    url(r'^login$', auth_views.login, {'template_name': 'hcapp/login.html'}, name='login'),
    #/hcapp/articles/
    url(r'^articles$', views.ArticleView.as_view(), name='articles'),
    # /hcapp/articles/create
    url(r'^articles/create$', views.ArticleCreation.as_view(), name='articles-create'),
    #hcapp/articles/$(article.id)
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view(), name='article-details'),
    # /hcapp/challenges/
    url(r'^challenges$', views.ChallengeView.as_view(), name='challenges'),
    # /hcapp/challenges/create
    url(r'^challenges/create$', views.ChallengeCreation.as_view(), name='challenge-create'),
    # hcapp/challenges/$(challenge.id)
    url(r'^challenges/(?P<pk>[0-9]+)/$', views.ChallengeDetail.as_view(), name='challenge-details'),
    # hcapp/menu-manager
    url(r'^menu-manager/$', views.MenuView.as_view(), name='menu-manager'),
    # hcapp/options
    url(r'^options/$', views.OptionsView.as_view(), name='options'),
]