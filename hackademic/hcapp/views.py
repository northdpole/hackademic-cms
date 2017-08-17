from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout

from .models import DbUser, DbArticle, DbChallenge
from .forms import UserForm
from django.views.generic import View, TemplateView, CreateView, FormView, RedirectView
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
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
        self.object = form.save(commit=False)
        self.object.slug = form.cleaned_data['title']
        self.object.save()
        return redirect('hcapp:articles')

class ChallengeView(generic.ListView):
    template_name = 'hcapp/challenges.html'
    context_object_name = 'all_challenges'

    def get_queryset(self):
        return DbChallenge.objects.all()


class ChallengeCreation(CreateView):
    model = DbChallenge
    fields = ['title', 'pkg_name', 'description', 'author', 'category']
    template_name = 'hcapp/challenge-form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(unidecode(form.cleaned_data['title']))
        self.object.save()
        return redirect('hcapp:challenges')

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


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/hcapp'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'hcapp/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/hcapp'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)