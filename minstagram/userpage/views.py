from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserPageData, UserProfileData
from .forms import MakePostForm
# from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
)


# create my first view
def go_home(request):
    if request.user.is_anonymous():
        return render(request, "userpage/index.html")
    posts_list = UserPageData.objects.filter(user=request.user).order_by("-time_created")
    profile_data = UserProfileData.objects.filter(user=request.user)
    context_data = {
        "posts_list": posts_list,
        "profile_data": profile_data,
    }
    return render(request, "userpage/myposts.html", context_data)


def regok(request):
    return render(request, "registration/OK.html")


def register(request, form=UserCreationForm()):
    if request.method == 'POST':
        data = UserCreationForm(request.POST)
        if data.is_valid():
            data.save()
        return HttpResponseRedirect("/registered-ok/")

    return render(request, "registration/signup.html", {"form": form})


def see_about(request):
    if request.user.is_anonymous():
        return render(request, "userpage/index.html")
    return render(request, "userpage/about.html")


def see_post(request, id=None):
    details_post = get_object_or_404(UserPageData, id=id)
    context_data = {
        "details_post": details_post,
    }
    return render(request, "userpage/mysubpost.html", context_data)


@login_required
def create_post(request):
    user_page_data = UserPageData(user=request.user)
    form = MakePostForm(request.POST or None, request.FILES or None, instance=user_page_data)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    context_data = {
        "form": form
    }
    return render(request, "userpage/create_post.html", context_data)


@login_required
def edit_post(request, id=None):
    edt_post = get_object_or_404(UserPageData, id=id)
    form = MakePostForm(request.POST or None, request.FILES or None, instance=edt_post)
    if form.is_valid():
        edt_post = form.save(commit=False)
        edt_post.save()
    context_data = {
        "upd_post": edt_post,
        "form": form,
    }
    return render(request, "userpage/edit_post.html", context_data)


@login_required
def delete_post(request, id=None):
    post = get_object_or_404(UserPageData, id=id)
    post.delete()
    return redirect("minstagram:home")


@login_required
def see_friends(request):
    context_data = {
        "following": request.user.userprofiledata.subscriptions.all(),
    }
    return render(request, "userpage/friends.html", context_data)


@login_required
def find_friends(request):
    profile_data = UserProfileData.objects.filter(~Q(user=request.user))
    following = request.user.userprofiledata.subscriptions.all()
    context_data = {
        "profile_data": profile_data,
        "following": following,
    }
    return render(request, "userpage/search.html", context_data)


@login_required
def see_user(request, id=None):
    user = get_object_or_404(User, id=id)
    query = UserPageData.objects.filter(user=user).order_by("-time_created")
    context_data = {
        "posts_list": query,
        "user_identification": id,
    }
    return render(request, "userpage/someonesposts.html", context_data)


@login_required
def see_user_post(request, user_id=None, post_id=None):
    details_post = get_object_or_404(UserPageData.objects.filter(user_id=user_id), id=post_id)
    context_data = {
        "details_post": details_post,
    }
    return render(request, "userpage/someonessubpost.html", context_data)


@login_required
def follow(request, id=None):
    user = User.objects.get(id=id)
    request.user.userprofiledata.subscriptions.add(user)
    return redirect("minstagram:find_friends")


@login_required
def unfollow(request, id=None):
    user = User.objects.get(id=id)
    request.user.userprofiledata.subscriptions.remove(user)
    return redirect("minstagram:see_friends")
