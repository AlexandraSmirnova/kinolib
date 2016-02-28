# encoding: utf-8
import hashlib
import random

import Image
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
# import plotly.plotly as py
import django.core.mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from jinja2 import utils
from forms import *
from models import *


class Main(ListView):
    queryset = Film.objects.order_by("-f_name").filter(f_flag=0)
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        return context


class FilmListByDate(ListView):
    queryset = Film.objects.order_by('-f_pub_date').filter(f_flag=0)[:20]
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(FilmListByDate, self).get_context_data(**kwargs)
        return context


class FilmListByRating(ListView):
    queryset = Film.objects.order_by('-f_rating').filter(f_flag=0)[:20]
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(FilmListByRating, self).get_context_data(**kwargs)
        return context


class FilmListByScores(ListView):
    queryset = Film.objects.annotate(num_scores=Count("score_film")).order_by('-num_scores').filter(f_flag=0)[:20]
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(FilmListByScores, self).get_context_data(**kwargs)
        return context


def login(request):
    context = {}
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("main"))
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
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("main"))
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
                                48hours http://95.213.199.8/confirm/%s" % (username, activation_key)

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
        context['comments'] = Comment.objects.filter(film=self.object).filter(c_flag=0)
        return context


@login_required
def add_comment(request):
    import json
    if request.method == 'POST':
        response_data = {}
        film = Film.objects.get(pk=request.POST.get('film'))
        post_text = str(utils.escape(request.POST.get('the_post'))).encode('utf-8')

        post = Comment(c_text=post_text, author=request.user, film=film)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.c_text
        response_data['created'] = post.c_pub_date.strftime(' %b. %d, %Y, %I:%M %P')
        response_data['author'] = post.author.username

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


@login_required
def hide_comment(request):
    import json
    if request.method == 'POST':
        response_data = {}
        flag = int(request.POST.get('flag'))
        comment = Comment.objects.get(pk=request.POST.get('id'))

        comment.c_flag = flag
        comment.save()

        response_data['id'] = comment.pk
        response_data['flag'] = flag

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"result": "nothing has happened"}), content_type="application/json")


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
        name = str(utils.escape(request.POST.get('name')))
        year = str(utils.escape(request.POST.get('year')))
        discript = str(utils.escape(request.POST.get('discription')))

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


@login_required
def add_score(request):
    import json
    response_data = {}
    if request.method == 'POST':

        film_id = int(request.POST.get('id'))
        mark = int(request.POST.get('mark'))
        try:
            film = Film.objects.get(pk=film_id)
            scores = Score.objects.filter(film=film_id)
            user_score = scores.filter(voter=request.user.id)

            if user_score.count() == 0:
                print(user_score.count())
                print(mark)
                print(film_id)
                print(request.user.id)
                new_score = Score(value=mark, film=film, voter=request.user)
                new_score.save()
                response_data['message'] = u"Спасибо за оценку"
            else:
                new_score = user_score[0]
                new_score.value = mark
                new_score.save()
                response_data['message'] = u"Ваша оценка изменена"
            film.f_rating = Score.objects.filter(film=film_id).aggregate(Avg('value'))['value__avg']
            film.save()
            response_data['rating'] = film.f_rating
        except Exception:
            response_data['message'] = str(Exception.message)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['message'] = "nothing has happened"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def statistic(request, film_id):
    context = {}
    x = Score.objects.values('value').filter(film=film_id)
    new_arr = []
    for num in x:
        new_arr.append(num['value'])

    make_histogram(new_arr, 'Histogram of scores')
    context['film_id'] = film_id
    return render(request, 'statistic.html', context)


@login_required
def user_statistic(request):
    context = {}
    x = Score.objects.values('value').filter(voter=request.user.id).filter(film__f_flag=0)
    new_arr = []
    for num in x:
        new_arr.append(num['value'])
    make_histogram(new_arr, 'Histogram of my scores')
    return render(request, 'statistic.html', context)


def make_histogram(x, title):
    n_bins = range(1, 11)
    fig = plt.figure()
    ax0 = plt.subplot()

    colors = ['red']
    ax0.hist(x, n_bins, histtype='bar', normed=1, color=colors, label=['scores'])
    ax0.axis([1, 10, 0, 1])
    # ax0.legend(prop={'size': 10})
    ax0.set_title(title)

    # plt.tight_layout()
    # file = PdfPages('static/img/testplot.png')
    plt.savefig('static/img/testplot.png')
    # mage.open('static/img/testplot.png').save('static/img/testplot.jpg', 'JPEG')
    plt.close(fig)
    return
