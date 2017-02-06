from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request):
    posts_available = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts_collection': posts_available})

@login_required
def post_draft_list(request):
    draft_posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'draft_posts_list': draft_posts})

def post_detail(request,pk):
        post_detail_retrieved = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post_detail_todisplay' : post_detail_retrieved})

@login_required
def post_new(request):
    if request.method == "POST":
        new_form=PostForm(request.POST)
        if new_form.is_valid():
            post=new_form.save(commit=False)
            post.author=request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        new_form = PostForm()
    return render(request, 'blog/post_edit.html', {'template_form': new_form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        edit_form=PostForm(request.POST, instance=post)
        if edit_form.is_valid():
            post=edit_form.save(commit=False)
            post.author=request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        edit_form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'template_form': edit_form})

@login_required
def post_publish(request,pk):
    post_detail_retrieved = get_object_or_404(Post, pk=pk)
    post_detail_retrieved.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request,pk):
    post_detail_retrieved = get_object_or_404(Post, pk=pk)
    post_detail_retrieved.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post_detail_retrieved = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        edit_form = CommentForm(request.POST)
        if edit_form.is_valid():
            comment = edit_form.save(commit=False)
            comment.post = post_detail_retrieved
            comment.save()
            return redirect('post_detail', pk=post_detail_retrieved.pk)
    else:
        edit_form=CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'template_form': edit_form})

@login_required
def remove_comment(request,pk):
    comment_retrieved = get_object_or_404(Comment, pk=pk)
    post_pk = comment_retrieved.post.pk
    comment_retrieved.delete()
    return redirect('post_detail', pk=post_pk)

@login_required
def ok_comment(request,pk):
    comment_retrieved = get_object_or_404(Comment, pk=pk)
    post_pk = comment_retrieved.post.pk
    comment_retrieved.approve()
    return redirect('post_detail', pk=post_pk)
