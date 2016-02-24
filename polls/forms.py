# encoding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from polls.models import Film


class RegistrationForm(UserCreationForm):
    # username = forms.CharField(label="Your Name", widget = forms.TextInput())
    # sername = forms.CharField(label="Your Sername", widget = forms.TextInput({'class':"input-xlarge", 'placeholder':"*"}))
    # mail = forms.EmailField(label="Your Email", widget = forms.TextInput({'class':"input-xlarge", 'placeholder':"*"}))
    # email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Электронный адрес'}))
    # first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    # password = forms.CharField( widget = forms.PasswordInput())
    # passwordSecond = forms.CharField(label="Input password again", widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in (forms.TextInput, forms.PasswordInput, forms.EmailInput):
                    field.widget = forms.TextInput(attrs={
                            'placeholder': field.label,
                            'class': 'form-block__input'
                        })

    # clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Такой адрес электронной почты уже зарегестрирован.')

    # modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.is_active = False  # not active until he opens activation link
            user.save()

        return user


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film

        fields = ('f_name', 'f_discription', 'f_year_creation')
        widgets = {
            'f_discription': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': u"Описание",
                    'class': 'form-block__input',
                    'required': True,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in (forms.TextInput, forms.NumberInput):
                    field.widget = forms.TextInput(attrs={
                            'placeholder': field.label,
                            'class': 'form-block__input',
                            'required': True,
                        })