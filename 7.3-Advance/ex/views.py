from urllib import request

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
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