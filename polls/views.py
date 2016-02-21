# encoding: utf-8
from django.shortcuts import  get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from forms import *
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone


class Main(ListView):
    #model = Film
    queryset = Film.objects.order_by("-f_name")
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        return context


class FilmListByDate(ListView):
    queryset = Film.objects.order_by('-f_pub_date')
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(FilmListByDate, self).get_context_data(**kwargs)
        return context


class FilmListByRating(ListView):
    queryset = Film.objects.order_by('-f_rating')
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(FilmListByRating, self).get_context_data(**kwargs)
        return context


def login(request):
    context = {}
    if request.POST:
        email = request.POST['email']
        try:
            name = User.objects.get(email=email)
            user1= auth.authenticate(username=name, password=password)
            if user1 is not None:
                auth.login(request, user1)
                return redirect('/')
        except:
            context['error'] = "Login or password is incorrect"
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)


def register(request):
    context = {}
    form = RegistrationForm()
    #if request.user.is_authenticated:
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

            send_mail(email_subject, email_body, 'myemail@example.com',
                      [email], fail_silently=False)

        return render(request, 'registration.html', context)
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
    context['title'] = "Congratulations!"
    context['message'] = "You has been activated"
    return render(request, 'message.html', context)


class FilmItem(DetailView):
    model = Film
    template_name = "film.html"

    def get_context_data(self, **kwargs):
        context = super(FilmItem, self).get_context_data(**kwargs)
        context["max_raiting"] = range(1,11)
        return context
