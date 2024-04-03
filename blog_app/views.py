from django.shortcuts import render, get_object_or_404, redirect
from blog_app.models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog_app.forms import PostForm
from taggit.models import Tag
from django.contrib.auth import get_user_model


def post_list(request):
    posts = Post.objects.all().order_by('id')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'posts': posts, "page": page})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_list')
        else:
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'create_post.html', {'form': form})


def posts_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    posts = Post.objects.filter(tagged_items__tag_id__in=[tag.id])
    return render(request, 'posts_by_tag.html', {'posts': posts, 'tag': tag})


def posts_by_author(request, author_name):
    UserModel = get_user_model()
    author = UserModel.objects.get(username=author_name)
    posts = Post.objects.filter(author=author)
    return render(request, 'posts_by_author.html', {'posts': posts, 'author': author})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})
