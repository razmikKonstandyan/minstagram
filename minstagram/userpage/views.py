from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserPageData
from .forms import MakePostForm


# create my first view


def go_home(request):
    query = UserPageData.objects.all().order_by("-time_created")
    context_data = {
        "posts_list": query,
    }
    return render(request, "minstagram/index.html", context_data)


def see_about(request):
    return render(request, "minstagram/generic.html", {})


def see_post(request, id=None):
    details_post = get_object_or_404(UserPageData, id=id)
    context_data = {
        "details_post": details_post,
    }
    return render(request, "minstagram/post.html", context_data)


def create_post(request):
    form = MakePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    context_data = {
        "form": form
    }
    return render(request, "minstagram/create_post.html", context_data)


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
    return render(request, "minstagram/edit_post.html", context_data)


def delete_post(request, id=None):
    post = get_object_or_404(UserPageData, id=id)
    post.delete()
    return redirect("minstagram:home")


def test(request):
    return HttpResponse("asd")
