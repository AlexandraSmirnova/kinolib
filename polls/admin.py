from django.contrib import admin

# Register your models here.

from .models import UserProfile
from .models import Film
from .models import Comment
from .models import Score

admin.site.register(UserProfile)
admin.site.register(Film)
admin.site.register(Comment)
admin.site.register(Score)