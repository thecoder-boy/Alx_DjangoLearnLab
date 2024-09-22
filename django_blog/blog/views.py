from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


class PostSearchView(ListView):
    model = Post
    template_name = "blog/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("query")
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "blog/login.html"


class CustomLogoutView(LogoutView):
    template_name = "blog/logout.html"


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)
