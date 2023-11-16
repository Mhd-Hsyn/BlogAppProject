from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(Comments)
admin.site.register(UserJWTWhiteListToken)
