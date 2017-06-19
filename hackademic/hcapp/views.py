from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import generic

from hcapp.models import db_user, db_article, db_challenge
from .forms import UserForm
from django.views.generic import View, TemplateView, CreateView


class IndexView(TemplateView):
    template_name = 'hcapp/index.html'


class ArticleView(generic.ListView):
    template_name = 'hcapp/articles.html'
    context_object_name = 'all_articles'

    def get_queryset(self):
        return db_article.objects.all()


class ArticleDetail(generic.DetailView):
    model = db_article
    template_name = 'hcapp/article-details.html'

class ArticleCreation(CreateView):
    model = db_article
    fields = ['title', 'content', 'created_by']
    template_name = 'hcapp/article-form.html'


class ChallengeView(generic.ListView):
    template_name = 'hcapp/challenges.html'
    context_object_name = 'all_challenges'

    def get_queryset(self):
        return db_challenge.objects.all()

class ChallengeCreation(CreateView):
    model = db_challenge
    fields = ['title', 'pkg_name', 'description', 'author', 'category']
    template_name = 'hcapp/challenge-form.html'


class ChallengeDetail(generic.DetailView):
    model = db_challenge
    template_name = 'hcapp/challenge-details.html'


class UserView(View):
    form_class = UserForm
    template_name = 'hcapp/register-form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit = False)

            #normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            user.set_password(password)
            user.save()

            #returns User  objects if credentials are correct

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('hcapp:index')
