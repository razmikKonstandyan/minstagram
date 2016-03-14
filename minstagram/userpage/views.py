from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserPageData, UserProfileData
from .forms import MakePostForm, EditInfo, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse


def go_home(request):
    """Method shows to a user his posts.

    Args:
        request: http request from the user.
    Returns:
        HttpResponse: http response that shows "userpage/myposts.html".
    """

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
    """Method indicates about successful registration.

    Args:
        request: http request from a user.
    Returns:
        HttpResponse: http response that shows "registration/OK.html".
    """
    return render(request, "registration/OK.html")


def register(request, form=UserRegistrationForm()):
    """Method allows a new user to sign up.

    Args:
        request: http request from the user.
    Returns:
        HttpResponse: http response that shows "registration/signup.html"
        if the form is not valid and does redirect to regok else.
    """
    if request.method == 'POST':
        data = UserRegistrationForm(request.POST)
        if data.is_valid():
            new_user = data.save()
            UserProfileData.objects.create(user=new_user, status="", avatar="\static\css\images\default.jpeg")
            return HttpResponseRedirect("/registered-ok/")
    return render(request, "registration/signup.html", {"form": form})


def see_about(request):
    """Method shows a page about Minstagram.

    Args:
        request: http request from a user.
    Returns:
        HttpResponse: http response that shows "userpage/index.html" with infromation
        about us if the user is not logged in and "userpage/about.html" else.
    """
    if request.user.is_anonymous():
        return render(request, "userpage/index.html")
    return render(request, "userpage/about.html")


def see_post(request, id=None):
    """Method allows users to see their specific post.

    Args:
        request: http request from a user.
        id: id of a specific post that the user wants to see.
    Returns:
        HttpResponse: http response that shows "userpage/mysubpost.html" with a
        chosen post.
    """
    details_post = get_object_or_404(UserPageData, id=id)
    return render(request, "userpage/mysubpost.html", {"details_post": details_post})


@login_required
def create_post(request):
    """Method allows users to create a new post.

    Args:
        request: http request from a user.
    Returns:
        HttpResponse: http response that shows "userpage/myposts.html" with
        a new post if the form is valid and "userpage/create_post.html" else.
    """

    user_page_data = UserPageData(user=request.user)
    form = MakePostForm(request.POST or None, request.FILES or None, instance=user_page_data)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        posts_list = UserPageData.objects.filter(user=request.user).order_by("-time_created")
        profile_data = UserProfileData.objects.filter(user=request.user)
        context_data = {
            "posts_list": posts_list,
            "profile_data": profile_data,
        }
        return render(request, "userpage/myposts.html", context_data)
    return render(request, "userpage/create_post.html", {"form": form})


@login_required
def edit_post(request, id=None):
    """Method allows users to edit their post.

    Args:
        request: http request from a user.
        id: id of a specific post that a user wants to edit.
    Returns:
        HttpResponse: http response that shows "userpage/myposts.html" with
        edited post if the form is valid and "userpage/edit_post.html" else.
    """
    edt_post = get_object_or_404(UserPageData, id=id)
    form = MakePostForm(request.POST or None, request.FILES or None, instance=edt_post)
    if form.is_valid():
        edt_post = form.save(commit=False)
        edt_post.save()
        posts_list = UserPageData.objects.filter(user=request.user).order_by("-time_created")
        profile_data = UserProfileData.objects.filter(user=request.user)
        context_data = {
            "posts_list": posts_list,
            "profile_data": profile_data,
        }
        return render(request, "userpage/myposts.html", context_data)
    context_data = {
        "upd_post": edt_post,
        "form": form,
    }
    return render(request, "userpage/edit_post.html", context_data)


@login_required
def delete_post(request, id=None):
    """Method allows users to delete their post.

    Args:
        request: http request from a user.
        id: id of a specific post that a user wants to delete.
    Returns:
        HttpResponse: http response that shows "userpage/myposts.html" without
        deleted post.
    """
    post = get_object_or_404(UserPageData, id=id)
    post.delete()
    return redirect("minstagram:home")


@login_required
def see_friends(request):
    """Method allows users to see their following.

    Args:
        request: http request from a user.
    Returns:
        HttpResponse: http response that shows "userpage/search.html" that
        contains following.
    """
    subscriptions = request.user.userprofiledata.subscriptions.all()
    following = UserProfileData.objects.filter(user__in=subscriptions)
    return render(request, "userpage/friends.html", {"following": following})


@login_required
def find_friends(request):
    """Method allows users to look for new friends.

    Args:
        request: http request from a user.
    Returns:
        HttpResponse: http response that shows "userpage/search.html" that
        contains all users.
    """
    profile_data = UserProfileData.objects.filter(~Q(user=request.user))
    following = request.user.userprofiledata.subscriptions.all()
    context_data = {
        "profile_data": profile_data,
        "following": following,
    }
    return render(request, "userpage/search.html", context_data)


@login_required
def see_user(request, id=None):
    """Method allows users to see someones page.

    Args:
        request: http request from a user.
        id: id of a specific user that the previous one wants to see.
    Returns:
        HttpResponse: http response that shows "userpage/someonesposts.html" that
        contains posts of a user with a choosen user id.
    """
    user = get_object_or_404(User, id=id)
    query = UserPageData.objects.filter(user=user).order_by("-time_created")
    following = request.user.userprofiledata.subscriptions.all()
    profile_data = UserProfileData.objects.filter(user=user)
    context_data = {
        "posts_list": query,
        "user_identification": id,
        "profile_data": profile_data,
        "following": following,
    }
    return render(request, "userpage/someonesposts.html", context_data)


@login_required
def see_user_post(request, user_id=None, post_id=None):
    """Method allows users to see someones specific post.

    Args:
        request: http request from a user.
        id: id of a specific user that the previous one wants to see.
        post_id: id of a specific post that the previous one wants to see.
    Returns:
        HttpResponse: http response that shows "userpage/someonessubpost.html" with a
        chosen post.
    """
    details_post = get_object_or_404(UserPageData.objects.filter(user_id=user_id), id=post_id)
    return render(request, "userpage/someonessubpost.html", {"details_post": details_post})


@login_required
def follow(request, id=None):
    """Method allows users to unfollow other users.

    Args:
        request: http request from a user.
        id: id of a specific user that the previous one wants to unfollow.
    Returns:
        HttpResponse: http response that shows to a user a page he did
        a request from.
    """
    user = User.objects.get(id=id)
    request.user.userprofiledata.subscriptions.add(user)
    return redirect(request.META["HTTP_REFERER"])


@login_required
def unfollow(request, id=None):
    """Method allows users to follow other users.

    Args:
        request: http request from a user.
        id: id of a specific user that the previous one wants to follow.
    Returns:
        HttpResponse: http response that shows to a user a page he did
        a request from.
    """
    user = User.objects.get(id=id)
    request.user.userprofiledata.subscriptions.remove(user)
    return redirect(request.META["HTTP_REFERER"])


@login_required
def edit_info(request):
    """Method allows users to change their profile info.

    Args:
        request: http request from a user.
    Returns:
        HttpResponse: http response that shows "userpage/mypost.html" to the client with
        updated profile info if the form is valid and "userpage/edit_info.html" else.
    """
    user_profile_data = UserProfileData.objects.get(user=request.user)
    profile_data = UserProfileData.objects.filter(user=request.user)
    form = EditInfo(request.POST or None, request.FILES or None, instance=user_profile_data)
    if form.is_valid():
        info = form.save(commit=False)
        info.save()
        posts_list = UserPageData.objects.filter(user=request.user).order_by("-time_created")
        context_data = {
            "posts_list": posts_list,
            "profile_data": profile_data,
        }
        return render(request, "userpage/myposts.html", context_data)
    return render(request, "userpage/edit_info.html", {"form": form})
