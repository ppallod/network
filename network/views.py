from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Like, Follower


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    page_obj = Paginator(posts, 10)

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    return render(request, "network/index.html", {
        'posts':page_obj.page(page),
        'page_obj':page_obj.page(page),
        'has_next': page_obj.page(page).has_next(),
        'has_previous': page_obj.page(page).has_previous(),
        'request': request
    })


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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new(request):
    if request.method == 'GET':
        return render(request,"network/newpost.html")
    
    if request.method == 'POST':
        text = request.POST["post"]
        user = request.user 
        post = Post(user=user, text=text)
        post.save()        
        return HttpResponseRedirect(reverse('index'))

def profile(request, id):
    if request.method == "GET":
        user = User.objects.get(pk=id)
        followers = user.followers.count()
        following = user.following.count()
        posts = Post.objects.filter(user=user).order_by('-timestamp').all()

        page_obj = Paginator(posts, 10)

        try:
            page = int(request.GET['page'])
        except:
            page = 1

        if request.user.id != id:
            following_flag = request.user.following.filter(following=id)
        else:
            following_flag = "self"
                
        return render(request, "network/profile.html", {
            'profile_user': user,
            'followers': followers,
            'following': following,
            'posts': page_obj.page(page),
            'following_flag': following_flag,
            'page_obj':page_obj.page(page),
            'has_next': page_obj.page(page).has_next(),
            'has_previous': page_obj.page(page).has_previous()
        })
    
    elif request.method == "POST":
        following_button = request.POST.get("following_button")
        if following_button == "True":
            following = request.user.following.get(following=id)
            following.delete()
        else:
            Follower(follower=request.user, following=User.objects.get(pk=id)).save()
            
        return HttpResponseRedirect(reverse('profile', args=(id,)))
    
def allposts(request):

    posts = Post.objects.all().order_by('-timestamp')
    page_obj = Paginator(posts, 10)

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    return render(request, "network/index.html", {
        'posts':page_obj.page(page),
        'page_obj':page_obj.page(page),
        'has_next': page_obj.page(page).has_next(),
        'has_previous': page_obj.page(page).has_previous(),
        'request': request
    })

def like(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        flag = data.get("flag")
        id = data.get("id")
        post = Post.objects.get(id=id)
        user = request.user        

        if flag == "dislike":
            like = Like.objects.filter(user=user, post=post).delete()
            return JsonResponse({'total_likes':post.total_likes})
        elif flag == "like":
            Like.objects.create(user=user, post=post).save()
            return JsonResponse({'total_likes':post.total_likes})
        else:
            print(f"Unknown flag - {flag}")
            return JsonResponse({'error':'Unknown flag'})
    else:
        return JsonResponse({'error':'An error occurred'})
 
def following(request):

    #Getting id for all the users that the current user follows
    following = request.user.following.all()
    if following is not None:
        following_ids = []
        for f in following:
            following_ids.append(f.following.id)
        posts = Post.objects.filter(user__in = following_ids).order_by('-timestamp')
    else:
        posts = None

    return render(request, "network/index.html", {
        'posts':posts
    })

def editpost(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        user = request.user
        post_id = data.get("post_id")
        text = data.get("text")

        post = Post.objects.filter(user=user,id=post_id).first()
        if post is not None:
            post.text = text
            post.save()
        else:
            JsonResponse({'error': 'Unauthorized'})

        return JsonResponse({'edited': True})
    else:
        return JsonResponse({'error':'invalid request method'})