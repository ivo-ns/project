from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from final_project.web.forms import SignUpForm, VinylAddForm
from final_project.web.models import Genre, Style, Vinyl, RecordLabel, Artist, Profile, Article

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    ordering = ('email',)
    list_display = ['email', 'date_joined', 'last_login']
    list_filter = ()
    add_form = SignUpForm
    readonly_fields = ('date_joined',)
    fieldsets = (
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'date_joined',),
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2",),
            },
        ),
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "age", "gender"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'date_added', 'headline', ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    ordering = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    ordering = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_display = ('name', 'genre',)


@admin.register(Vinyl)
class VinylAdmin(admin.ModelAdmin):
    form = VinylAddForm
    ordering = ('pk',)
    list_display = ('pk', 'artist', 'title', 'record_label', 'cat_number', 'style', 'condition', 'release_date',)


@admin.register(RecordLabel)
class RecordLabelAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }
    ordering = ('name',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }
    ordering = ('name',)
    list_display = ['name', 'slug', 'style', 'location', 'booking_fee_per_hour']
