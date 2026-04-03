from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import IntegrityError
from .models import Article, UserFavouriteArticle

# Articles view must show a HTML table

class Articles(ListView):
    model = Article
    template_name = "ex/articles_list.html"
    context_object_name = "articles"


    # descomentar al llegar a ex03
    # class Meta:
    #     ordering = ['-created']

class Home(RedirectView):
    url = reverse_lazy('ex:articles')

class Login(LoginView):
    template_name = "ex/login.html"
    def get_success_url(self):
        return reverse_lazy('ex:home')

class Publications(LoginRequiredMixin, ListView):
    model = Article
    template_name = "ex/publications.html"
    context_object_name = "articles"
    
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
    
    def handle_no_permission(self):
        return redirect('ex:login')
    
class Detail(LoginRequiredMixin, DetailView):
    # only available for authors of the article????
    model = Article
    template_name = "ex/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return self.model.objects.filter(id=self.kwargs['pk'])
    
    def handle_no_permission(self):
        return redirect('ex:login')
    
class Logout(LogoutView):
    next_page = reverse_lazy('ex:home')

class Favourite(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    fields = ['article']
    template_name = "ex/favourite.html"
    success_url = reverse_lazy('ex:articles')
    context_object_name = "favourite_articles"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    

class Register(CreateView):
    form_class = UserCreationForm
    template_name = "ex/register.html"
    success_url = reverse_lazy('ex:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully. You can now log in.")
        return response
    

class Publish(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'synopsis', 'content']
    template_name = "ex/publish.html"
    success_url = reverse_lazy('ex:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('ex:article-detail', kwargs={'pk': self.object.pk})

class AddFavourite(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = []
    # template_name = "ex/add_favourite.html"
    success_url = reverse_lazy('ex:favourites')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs["pk"])
        try:
            return super().form_valid(form)
        except IntegrityError:
            return redirect("ex:article-detail", pk=self.kwargs["pk"])
        
    def get_success_url(self):
        return reverse_lazy("ex:article-detail", kwargs={"pk": self.kwargs["pk"]})






def debug(request):
    # print list of database tables
    from django.db import connection as dj_connection

    intros = dj_connection.introspection
    tables = []
    try:
        with dj_connection.cursor() as cursor:
            try:
                tables = intros.table_names(cursor)
            except TypeError:
                # some Django versions expect no cursor
                tables = intros.table_names()
    except Exception as e:
        tables = [f"Error listing tables: {e}"]

    print("DB tables:", tables)

    return HttpResponse(f"Debugging view - tables: {tables}")