from django.contrib import admin

from .models import User
from .models import BlacklistedToken
from .models import UserImage

admin.site.register(User)
admin.site.register(BlacklistedToken)
admin.site.register(UserImage)

