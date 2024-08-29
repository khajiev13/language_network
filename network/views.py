from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Post, Comment, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Handle image upload
        image = request.FILES.get("image")

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, first_name=first_name, last_name=last_name)
            if image:
                user.image = image
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def posts(request):
    # Save the post when a form is submitted
    if request.POST:
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        post = Post.objects.create(author=user, title=title, content=content)
        post.save()
        all_posts = Post.objects.order_by('-created_at')
        return render(request, "network/posts.html", {"posts": all_posts, "message": "Your post has been added sucessfully."})

    all_posts = Post.objects.order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 10)
    users = None
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/posts.html", {"posts": posts, 'page_obj': posts})


def new_comment(request, post_id):
    if request.POST:
        # Get the post and the author, content
        post = Post.objects.get(id=post_id)
        author = User.objects.get(id=request.user.id)
        content = request.POST['comment_input']
        # Create a new comment

        new_comment = Comment.objects.create(
            author=author, post=post, content=content)
        new_comment.save()
        all_posts = Post.objects.order_by('-created_at')
        return render(request, "network/posts.html", {"posts": all_posts, "message": "Your comment has been added sucessfully."})
    else:
        return None


def post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.POST:
        # Get the parent ID if there is one
        parent_id = request.POST['reply_to_comment_id']
        comment_content = request.POST['comment_input']
        author = User.objects.get(id=request.user.id)
        if len(parent_id) > 0:
            parent_comment = Comment.objects.get(id=parent_id)
            comment = Comment.objects.create(
                post=post, parent=parent_comment, author=author, content=comment_content)
        else:
            comment = Comment.objects.create(
                post=post, author=author, content=comment_content)
        comment.save()
        return render(request, "network/post.html", {"post": post, 'message': 'Your comment has been posted.'})

    return render(request, "network/post.html", {"post": post})


def user(request, user_id):
    user = User.objects.get(id=user_id)
    posts = user.posts.order_by('-created_at')
    if request.method == 'POST' and request.user.is_authenticated:
        follow_value = request.POST.get('follow')
        print(follow_value)
        if follow_value == "True":
            request.user.following.add(user)
            print('True')
        else:
            print('False')
            request.user.following.remove(user)
    if request.user in user.followers.all():
        followers = True
    else:
        followers = False
    context = {
        "user_info": user,
        'posts': posts,
        'followers': followers
    }
    return render(request, "network/user.html", context)


def following(request):
    posts = list()
    following = request.user.following.all()
    for follow in following:
        for each_post in follow.posts.all():
            posts.append(each_post)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    users = None
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        'page_obj': posts
    }
    return render(request, "network/following.html", context)


def toggle_like(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        liked = post.likes.filter(user=request.user).exists()
        if liked:
            post.likes.filter(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, post=post)
        return JsonResponse({'likes_count': post.likes.count()})
    return JsonResponse({'error': 'Unauthorized'}, status=401)


def edit_post(request, post_id):
    if request.method == "POST" and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.author:
            try:
                data = json.loads(request.body)
                post.title = data.get('title', '')
                post.content = data.get('content', '')
                post.save()
                return JsonResponse({'success': True, 'content': post.content, 'title': post.title})
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Unauthorized'}, status=401)


def message(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        return render(request, "network/message.html", {'user_info': user})
