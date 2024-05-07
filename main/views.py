from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages 
from .models import Profile, Post, LikePost, FollowersCount
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse 
from itertools import chain
from django.http import JsonResponse
import random
import requests
# from django.urls import reverse


# from chat.models import Thread

# Create your views here.

@login_required(login_url='login_or_register')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feeds_lists = Post.objects.filter(user=usernames)
        feed.append(feeds_lists)

    feed_list = list(chain(*feed))

    # Fetch profile images for each post
    for post in feed_list:
        post.profile_image = Profile.objects.get(user__username=post.user).profileimg

    #user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []
    
    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

@login_required(login_url='login_or_register')
def upload(request): 
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()


       
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='login_or_register')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list =[]

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list':username_profile_list})

@login_required(login_url='login_or_register')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.num_of_likes = post.num_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.num_of_likes = post.num_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='login_or_register')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)


    # Get the ID of the profile user
    other_user_id = user_profile.user.id

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'


    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text' : button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'other_user_id': other_user_id,  # Pass other_user_id to the context

    }
    return render(request, 'profile.html', context)

@login_required(login_url='login_or_register')
def follow(request):
   if request.method == 'POST':
       follower = request.POST['follower']
       user = request.POST['user']

       if FollowersCount.objects.filter(follower=follower, user=user).first():
           delete_follower = FollowersCount.objects.get(follower=follower, user=user)
           delete_follower.delete()
           return redirect('/profile/'+user)
       else:
           new_follower = FollowersCount.objects.create(follower=follower, user=user)
           new_follower.save()
           return redirect('/profile/'+user)

   else:
       
       return redirect('/')

@login_required(login_url='login_or_register')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg  = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg  = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')

    return render(request, 'setting.html',{'user_profile': user_profile})

   

@login_required(login_url='login_or_register')
def logout(request):
    auth.logout(request)
    return redirect('login_or_register')




def proxy_news(request):
    try:
        # Make a request to the News API
        response = requests.get('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       'apiKey=your api-key')
        data = response.json()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@login_required(login_url='signin')
def Library(request):
    return render(request, 'Library.html')

@login_required(login_url='signin')
def Book(request):
    return render(request, 'book.html')




def login_or_register(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            # Signup Logic
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('login_or_register')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username taken')
                    return redirect('login_or_register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    # Log user in and direct to settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    # Create profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()

                    return redirect('settings')
            else:
                messages.info(request, 'Passwords do not match!')
                return redirect('login_or_register')
        elif 'signin' in request.POST:
            # Signin Logic
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('login_or_register')
    return render(request, 'LoginorRegister.html')


