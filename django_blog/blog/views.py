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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy
# from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag


class TaggedPostListView(ListView):
    model = Post
    template_name = "tagged_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get("tag_slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = get_object_or_404(Tag, slug=self.kwargs.get("tag_slug"))
        return context


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "comment_form.html"
    context_object_name = "comment"

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user  # Ensure only the author can edit
        comment.save()
        return super().form_valid(form)

    def get_queryset(self):
        """Ensure that only the author can update their comment."""
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        """Redirect to the post detail page after a successful comment edit."""
        post_id = self.object.post.id
        return reverse_lazy("post_detail", kwargs={"pk": post_id})


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"
    context_object_name = "comment"

    def get_queryset(self):
        """Ensure that only the author can delete their comment."""
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        """Redirect to the post detail page after a successful comment deletion."""
        post_id = self.object.post.id
        return reverse_lazy("post_detail", kwargs={"pk": post_id})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture"]


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}

    return render(request, "blog/profile.html", context)


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
