from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required


def view_blog(request):
    ''' A view to show the blog page '''

    posts = Post.objects.all()
    template = "blog/view_blog.html"
    context = {
        "posts": posts,
    }

    return render(request,
                  template,
                  context)


def view_post(request, post_id):
    ''' Show the single post page and
        the comments and comments form to logged in users
    '''

    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            form.save()
            messages.success(request, "Your comment has been added.")
            return redirect(reverse("view_post", args=[post_id]))
        else:
            messages.error(request,
                           "Error adding your comment please try again")
            return redirect(reverse("view_post", args=[post_id]))
    comments = Comment.objects.filter(post=post)

    form = CommentForm()
    template = "blog/post.html"

    context = {
        "form": form,
        "post": post,
        "comments": comments,
    }

    return render(request,
                  template,
                  context)

