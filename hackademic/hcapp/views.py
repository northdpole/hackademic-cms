from .models import DbUser, DbArticle, DbChallenge
from .forms import UserForm
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import generic
from unidecode import unidecode
from django.template.defaultfilters import slugify


class IndexView(TemplateView):
    template_name = 'hcapp/index.html'

class MenuView(TemplateView):
    template_name = 'hcapp/menu-manager.html'

class OptionsView(TemplateView):
    template_name = 'hcapp/options.html'

class ArticleView(generic.ListView):
    template_name = 'hcapp/articles.html'
    context_object_name = 'all_articles'

    def get_queryset(self):
        return DbArticle.objects.all()


class ArticleDetail(generic.DetailView):
    model = DbArticle
    template_name = 'hcapp/article-details.html'


class ArticleCreation(CreateView):
    model = DbArticle
    fields = ['title', 'content', 'created_by']
    template_name = 'hcapp/article-form.html'

    def form_valid(self, form):
        DbArticle.slug = slugify(unidecode(self.title))
        return super(ArticleCreation, self).form_valid(form)

class ChallengeView(generic.ListView):
    template_name = 'hcapp/challenges.html'
    context_object_name = 'all_challenges'

    def get_queryset(self):
        return DbChallenge.objects.all()


class ChallengeCreation(CreateView):
    model = DbChallenge
    fields = ['title', 'pkg_name', 'description', 'author', 'category']
    template_name = 'hcapp/challenge-form.html'


class ChallengeDetail(generic.DetailView):
    model = DbChallenge
    template_name = 'hcapp/challenge-details.html'


class UserView(generic.ListView):
    template_name = 'hcapp/users.html'
    context_object_name = 'all_users'

    def get_queryset(self):
        return DbUser.objects.all()

class UserDetail(generic.DetailView):
    model = DbUser
    template_name = 'hcapp/users-details.html'

class UserCreation(View):
    form_class = UserForm
    template_name = 'hcapp/register-form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            user.slug = slugify(unidecode(username))
            user.set_password(password)
            user.save()

            # returns User  objects if credentials are correct

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('hcapp:index')

