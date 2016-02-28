from django.shortcuts import render, get_object_or_404, redirect
from .models import UserPageData
from .forms import MakePostForm
#from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
)


# create my first view
def go_home(request):
    if request.user.is_anonymous():
        return render(request, "minstagram/index.html")
    query = UserPageData.objects.all().order_by("-time_created")
    context_data = {
        "posts_list": query,
    }
    return render(request, "minstagram/userpost.html", context_data)


def regok(request):
    return render(request, "registration/OK.html")


def register(request, form=UserCreationForm()):
    if request.method == 'POST':
        data = UserCreationForm(request.POST)
        if data.is_valid():
            data.save()
        return HttpResponseRedirect("/registered-ok/")

    return render(request, "registration/register.html", {"form": form})


def see_about(request):
    if request.user.is_anonymous():
        return render(request, "minstagram/index.html")
    return render(request, "minstagram/about.html")


def see_post(request, id=None):
    details_post = get_object_or_404(UserPageData, id=id)
    context_data = {
        "details_post": details_post,
    }
    return render(request, "minstagram/userpost.html", context_data)

@login_required
def create_post(request):
    form = MakePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    context_data = {
        "form": form
    }
    return render(request, "minstagram/create_post.html", context_data)

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
    return render(request, "minstagram/edit_post.html", context_data)

@login_required
def delete_post(request, id=None):
    post = get_object_or_404(UserPageData, id=id)
    post.delete()
    return redirect("minstagram:home")