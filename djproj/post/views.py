import os
from django.shortcuts import render, redirect
from .models import Post
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from . import forms
# Create your views here.


def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', { 'posts': posts })

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    # commands = Comment.objects.filter(comment_post = post.id)
    # return render(request, 'posts/post_page.html', { 'post': post, 'post_comments': commands })
    html_file_path = None
    html_content = None
    if post and post.html_file:
        try:
            html_file_path = post.html_file.path  # Get the full file system path
            # Check if the file exists before attempting to open it
            if os.path.exists(html_file_path):
                with open(html_file_path, 'r') as file:
                    html_content = file.read()
            else:
                html_content = "File not found."  # Or handle this as you prefer
        except (ValueError, FileNotFoundError):
            html_content = "Error reading file."  # Or handle the error as you prefer

    context = {
        'post': post,
        'html_file_path': html_file_path,
        'html_content': html_content
        }
    return render(request, 'posts/post_page.html', context)

@login_required(login_url="/users/login/")
def post_new(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            # save with user
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('posts:list')
    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', { 'form': form })


@login_required(login_url="/users/login/")
def post_category_new(request):
    if request.method == "POST":
        form = forms.PostCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            # save with user
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('posts:new-post')
    else:
        form = forms.PostCategoryForm()
    return render(request, 'posts/postCategory_new.html', { 'form': form })

