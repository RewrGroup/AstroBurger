from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Jugada, Pote, Membership, Testimonio, SponsorsPorPote, IpsYCookies, Codigo


class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'
    extra = 1
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Jugada)
admin.site.register(Pote)
admin.site.register(Membership)
admin.site.register(Testimonio)
admin.site.register(SponsorsPorPote)
admin.site.register(IpsYCookies)
admin.site.register(Codigo)