# blog/views.py
from django.shortcuts import render, redirect, t, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileForm, PostForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment, Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.utils.text import slugify
from .forms import PostForm, CommentForm

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
        # process tags string
        tags_str = form.cleaned_data.get('tags', '')
        self._attach_tags(self.object, tags_str)
        return response

    def _attach_tags(self, post, tags_str):
        post.tags.clear()
        for raw in [t.strip() for t in tags_str.split(',') if t.strip()]:
            tag, _ = Tag.objects.get_or_create(name__iexact=raw, defaults={'name': raw, 'slug': slugify(raw)})
            # get_or_create with case-insensitive fallback if exists with different case
            if not tag.pk:
                tag = Tag.objects.filter(name__iexact=raw).first() or tag
            post.tags.add(tag)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # prefill tags as comma-separated names
        initial['tags'] = ', '.join([t.name for t in self.get_object().tags.all()])
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        tags_str = form.cleaned_data.get('tags', '')
        self._attach_tags(self.object, tags_str)
        return response

    def _attach_tags(self, post, tags_str):
        post.tags.clear()
        for raw in [t.strip() for t in tags_str.split(',') if t.strip()]:
            tag, created = Tag.objects.get_or_create(name__iexact=raw, defaults={'name': raw, 'slug': slugify(raw)})
            if not tag.pk:
                tag = Tag.objects.filter(name__iexact=raw).first() or tag
            post.tags.add(tag)


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
# -- Comment views --
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        # Link the comment to the current post and user
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_id']})


# --- comment edit & delete views (CBVs) ---
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

class TagDetailView(ListView):
    model = Post
    template_name = 'blog/tag_detail.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=slug)
        return tag.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return context

def search_view(request):
    q = request.GET.get('q', '').strip()
    results = Post.objects.none()
    if q:
        results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()
    return render(request, 'blog/search_results.html', {'query': q, 'results': results})
