from django.conf.urls import url
from . import views

app_name = 'hcapp'

urlpatterns = [
    #/hcapp/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #/hcapp/register/
    url(r'^register$', views.UserView.as_view(), name='register'),
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
]