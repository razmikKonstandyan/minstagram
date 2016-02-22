from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserPage
from .forms import MakePostForm


# create my first view

# create form for a new post

def create_post(request):
    form = MakePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    context_data = {
        "form": form
    }
    return render(request, "create_post.html", context_data)


def go_home(request):
    query = UserPage.objects.all()
    context_data = {
        "posts_list": query,
    }
    return render(request, "index.html", context_data)


def see_post(request, id=None):
    details_post = get_object_or_404(UserPage, id=id)
    context_data = {
        "details_post": details_post
    }
    return render(request, "post.html", context_data)


def see_about(request):
    return render(request, "generic.html", {})


def delete_post(request, id=None):
    post = get_object_or_404(UserPage, id)
    post.delete()
    return redirect("")


def test(request):
    return HttpResponse("asd")
