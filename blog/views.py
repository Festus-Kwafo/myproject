from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *

from taggit.models import Tag

# list of post view


def post_list(request, tag_slug=None):

    posts = Post.published.all()
    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 2)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog.html', {'posts': posts, page: 'pages'})

# detail of post view


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status=1)

    # list of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)

    if request.method == 'POST':
        # comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # redirect to same page and focus on that comment
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
        else:
            comment_form = CommentForm()

    return render(request, 'blog/article.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

# handling reply, reply view


def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input
            reply = form.save(commit=False)

            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url+'#'+str(reply.id))
    return redirect("/")
