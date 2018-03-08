# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse, Http404

# Create your views here.

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone

from blog.form import *
from blog.models import *

@login_required
def globalStream(request):
    posts = PostEntry.objects.all().reverse()
    context = {'posts': posts}
    return render(request, 'blog/globalStream.html', context)

@login_required
def followerStream(request):
    return render(request, 'blog/followerStream.html', {})


@login_required
def edit(request, id):
    item = Item.objects.select_for_update().filter(toUser=id)
    form = EditItemForm(request.POST, request.FILES, instance=item)
    if not form.is_valid():
        entry = Item.objects.filter(toUser=id)
        form = EditItemForm(instance=entry)
        context = { 'entry': entry, 'form': form }
        return render(request, 'blog/editProfile.html', context)

    context = { 'entry': entry, 'form': form }
    return render(request, 'blog/editProfile.html', context)


@login_required
def myProfile(request):
        context = {}

        # Just display the registration form if this is a GET request.
        if request.method == 'GET':
            if not Item.objects.filter(toUser=request.user.id):
                context['form'] = ItemForm()
                return render(request, 'blog/myProfile.html', context)
            else :
                item = Item.objects.filter(toUser=request.user.id)
                context['item'] = item
                return render(request, 'blog/editProfile.html', context)
        if request.method == 'POST':
            new_item = Item(toUser=request.user)
            form = ItemForm(request.POST, request.FILES, instance=new_item)
            if not form.is_valid():
                context['form'] = form
            else:
                # Must copy content_type into a new model field because the model
                # FileField will not store this in the database.  (The uploaded file
                # is actually a different object than what's return from a DB read.)
                new_item.content_type = form.cleaned_data['picture'].content_type
                form.save()
                context['form'] = ItemForm()

            context['items'] = Item.objects.filter(toUser=request.user.id)
            return render(request, 'blog/globalStream.html', context)

@login_required
def getProfile(request, userid):
        context = {}
        if request.method == 'GET':
            item = Item.objects.filter(toUser=userid)
            context['item'] = item
            return render(request, 'blog/getProfile.html', context)


def get_photo(request, id):
    item = get_object_or_404(Item, id=id)

    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)


@login_required
def postItem(request):
    errors = []

    # Adds the new item to the database if the request parameter is present
    if 'postItem' not in request.POST or not request.POST['postItem']:
        errors.append('You must enter an few words to post.')
    else:
        new_post = PostEntry(post_content=request.POST['postItem'],
                        first_name=request.user.first_name,
                        last_name=request.user.last_name,
                        post_user = request.user,
                        post_time=timezone.now())
        new_post.save()

    # Sets up data needed to generate the view, and generates the view
    posts = PostEntry.objects.all().reverse()
    context = {'posts': posts, 'errors': errors}
    return render(request, 'blog/globalStream.html', context)

@login_required
def commentItem(request, pk):
    errors = []
    post = PostEntry.objects.get(id=pk)
    # Adds the new item to the database if the request parameter is present
    if 'commentItem' not in request.POST or not request.POST['commentItem']:
        errors.append('You must enter an few words to comment.')
    else:
        new_comment = CommentEntry(comment_content=request.POST['commentItem'],
                        first_name=request.user.first_name,
                        last_name=request.user.last_name,
                        comment_time=timezone.now(),
                        comment_user=request.user,
                        toPost= post )

        new_comment.save()

    # Sets up data needed to generate the view, and generates the view
    posts = PostEntry.objects.all().reverse()
    context = {'posts': posts, 'errors': errors}
    return render(request, 'blog/globalStream.html', context)


def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'blog/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'blog/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))
