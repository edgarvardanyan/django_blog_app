from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Comment
from django.utils import timezone
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # fieldname__lte: field value must be less than or equal to
        # order_by('-published_date'): the - sign is for the decreading order
        return Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


# The user most be logged in for seeing some views
# In this cases I inherit from LoginRequiredMixin
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    # Same features as the CreatePostView
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # using reverse_lazy so that url is not called before deleting
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        # only show unpublished posts
        return Post.objects.filter(
            published_date__isnull=True).order_by('-create_date')


@login_required
def post_publish(request, pk):
    # get the post, publish, and go to its detail page
    post = get_object_or_404(Post, pk=pk)
    post.publish()

    return redirect('post_detail', pk=pk)

######################################
#       the views for comments       #
######################################


def add_comment_to_post(request, pk):
    # get the post or return Error 404
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # get the comment, set the post and save it
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # set an empty form id method is not POST
        form = CommentForm()

    return render(request, 'blog/comment_form.html', context={'form': form})


@login_required
def comment_approve(request, pk):
    # get the comment by its primary key or Error 404
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()

    # redirect to the corresponfing post after approval
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    # get the comment by its primary key or Error 404
    comment = get_object_or_404(Comment, pk=pk)

    # get the post pk before deleting the comment
    post_pk = comment.post.pk
    comment.delete()

    # go to the post page
    return redirect('post_detail', pk=post_pk)
