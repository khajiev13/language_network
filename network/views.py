from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User, Post, Comment


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
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
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
        post = Post.objects.create(author=user,title=title,content=content)
        post.save()
        all_posts = Post.objects.order_by('-created_at')
        return render(request, "network/posts.html", {"posts":all_posts, "message": "Your post has been added sucessfully."})

    all_posts = Post.objects.order_by('-created_at')
    return render(request, "network/posts.html", {"posts":all_posts})


def new_comment(request,post_id):
    if request.POST:
        # Get the post and the author, content
        post = Post.objects.get(id=post_id)
        author = User.objects.get(id= request.user.id)
        content = request.POST['comment_input']
        # Create a new comment

        new_comment = Comment.objects.create(author=author,post=post, content=content)
        new_comment.save()
        all_posts = Post.objects.order_by('-created_at')
        return render(request, "network/posts.html", {"posts":all_posts, "message": "Your comment has been added sucessfully."})
    else:
        return None
    

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "network/post.html",{"post": post})