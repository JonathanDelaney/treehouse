from django.contrib import admin
from .models import UsersFavourites


class UsersFavouritesAdmin(admin.ModelAdmin):
    model = UsersFavourites
    list_display = (
        "user",
    )


admin.site.register(UsersFavourites, UsersFavouritesAdmin)
