# blog/views.py
from django.shortcuts import render, redirect, t, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileForm, PostForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# -- Post views --
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # templates/blog/post_list.html
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # include an empty form for inline comment posting
        context['comment_form'] = CommentForm()
        # we can access comments via related_name 'comments'
        context['comments'] = self.object.comments.all().order_by('created_at')
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # set the author automatically
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# -- Authentication views (if not already present) --
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('post-list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', {'user_form': uform, 'profile_form': pform})


@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment posted.')
        else:
            # if invalid, show errors on post detail (optional: store errors in session/message)
            messages.error(request, 'There was a problem with your comment.')
    return redirect(post.get_absolute_url())

# --- comment edit & delete views (CBVs) ---
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.get_object().post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        # after deleting, redirect to the post's detail page
        post = self.get_object().post
        return post.get_absolute_url()

