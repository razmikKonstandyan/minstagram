from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import UserPageData
from .forms import MakePostForm
from django.db.models import Q


# create my first view


def go_home(request):
    query = UserPageData.objects.filter(user=request.user).order_by("-time_created")
    context_data = {
        "posts_list": query,
    }
    return render(request, "userpage/index.html", context_data)


def see_about(request):
    return render(request, "userpage/generic.html", {})


def see_post(request, id=None):
    details_post = get_object_or_404(UserPageData, id=id)
    context_data = {
        "details_post": details_post,
    }
    return render(request, "userpage/post.html", context_data)


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


def delete_post(request, id=None):
    post = get_object_or_404(UserPageData, id=id)
    post.delete()
    return redirect("minstagram:home")


def find_friends(request):
    query = User.objects.filter(~Q(id=request.user.id))
    context_data = {
        "users_list": query
    }
    return render(request, "userpage/search.html", context_data)


def see_friends(request):
    return HttpResponse("jkh")


def see_user(request, id=None):
    user = get_object_or_404(User, id=id)
    query = UserPageData.objects.filter(user=user).order_by("-time_created")
    context_data = {
        "posts_list": query,
        "user_identification": id,
    }
    return render(request, "userpage/see_user.html", context_data)


def see_user_post(request, user_id = None, post_id=None):
    details_post = get_object_or_404(UserPageData, id=post_id)
    context_data = {
        "details_post": details_post,
    }
    return render(request, "userpage/see_user_post.html", context_data)

