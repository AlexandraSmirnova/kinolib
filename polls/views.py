# encoding: utf-8
import datetime
import hashlib
import random

import django.core.mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView

from forms import *
from models import *


class Main(ListView):
    # model = Film
    queryset = Film.objects.order_by("-f_name").filter(f_flag=0)
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        return context


class FilmListByDate(ListView):
    queryset = Film.objects.order_by('-f_pub_date').filter(f_flag=0)
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(FilmListByDate, self).get_context_data(**kwargs)
        return context


class FilmListByRating(ListView):
    queryset = Film.objects.order_by('-f_rating').filter(f_flag=0)
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(FilmListByRating, self).get_context_data(**kwargs)
        return context


def login(request):
    context = {}
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user1 = auth.authenticate(username=user.username, password=password)
            if user1 is not None:
                auth.login(request, user1)
                return redirect('/')
        except Exception:
            context['error'] = "Email or password is incorrect"
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)


def register(request):
    context = {}
    form = RegistrationForm()
    context['title'] = u'Регистрация'
    context['form_url'] = '/reg'
    # if request.user.is_authenticated:
    #    return HttpResponseRedirect(reverse("main"))
    if request.POST:
        form = RegistrationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Get user by username
            user = User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Подтверждение регистрации'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
                                48hours http://kinolib.com/confirm/%s" % (username, activation_key)

            django.core.mail.send_mail(email_subject, email_body, 'myemail@example.com',
                                       [email], fail_silently=False)
            context['title'] = u"Подтверждение регистрации"
            context['message'] = u"На указанный почтовый ящик для подтверждения регистрации было отправлено письмо"
            return render(request, 'message.html', context)
    else:
        context['form'] = form
    return render(request, 'registration.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register_confirm(request, key):
    context = {}
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=key)

    # check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        context['title'] = "Sorry!"
        context['message'] = "Your key was expired"
        return render(request, 'message.html', context)
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    context['title'] = u"Ура!"
    context['message'] = u"Спасибо за подтверждение регистрации"
    return render(request, 'message.html', context)


@login_required
def new_film(request):
    context = {}
    form = FilmForm()
    context['title'] = u'Новый фильм'
    context['form_url'] = '/new_film'
    if request.POST:
        form = FilmForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        context['form'] = form
    return render(request, 'registration.html', context)


class FilmItem(DetailView):
    model = Film
    template_name = "film.html"

    def get_context_data(self, **kwargs):
        context = super(FilmItem, self).get_context_data(**kwargs)
        context['max_raiting'] = range(1, 11)
        context['comments'] = Comment.objects.filter(film=self.object)
        return context


@login_required
def add_comment(request):
    import json
    if request.method == 'POST':
        response_data = {}
        film = Film.objects.get(pk=request.POST.get('film'))
        post_text = request.POST.get('the_post')

        post = Comment(c_text=post_text, author=request.user, film=film)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.c_text
        response_data['created'] = post.c_pub_date.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


@login_required
def delete_restore(request):
    import json
    if request.method == 'POST':
        response_data = {}
        flag = int(request.POST.get('flag'))
        film = Film.objects.get(pk=request.POST.get('id'))

        film.f_flag = flag
        film.save()

        response_data['id'] = film.pk
        response_data['flag'] = flag

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"result": "nothing has happened"}), content_type="application/json")


@login_required
def update(request):
    import json
    if request.method == 'POST':
        response_data = {}

        film = Film.objects.get(pk=request.POST.get('film'))
        name = str(request.POST.get('name'))
        year = str(request.POST.get('year'))
        discript = str(request.POST.get('discription'))

        if name:
            film.f_name = name
        if year:
            film.f_year_creation = year
        if discript:
            film.f_discription = discript
        film.save()

        response_data['name'] = film.f_name
        response_data['year'] = film.f_year_creation
        response_data['discription'] = film.f_discription

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"result": "nothing has happened"}), content_type="application/json")
