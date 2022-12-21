from enum import Enum

from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from smart_selects.db_fields import ChainedForeignKey

from final_project import settings
from final_project.web.managers import AppUserManager
from final_project.web.mixins import ChoicesEnumMixin
from final_project.web.utils import validate_alphabet_characters_english, get_upload_path
from final_project.web.validators import validate_only_letters, age_validator
from thumbnails.fields import ImageField


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        validators=[
            validate_alphabet_characters_english,
        ])
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'

    objects = AppUserManager()


class Genre(models.Model):
    name = models.CharField(
        max_length=222
    )
    slug = models.SlugField(
        unique=True, null=True
    )
    description = models.TextField()

    image = models.ImageField(
        upload_to='genres/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Style(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.RESTRICT
    )
    name = models.CharField(
        max_length=222
    )
    slug = models.SlugField(
        unique=True,
        null=True
    )
    description = models.TextField()

    image = models.ImageField(
        upload_to='styles/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class RecordLabel(models.Model):
    name = models.CharField(
        max_length=222,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    website = models.URLField(
        max_length=100,
        null=True,
        blank=True
    )
    logo = ImageField(
        upload_to='record_labels/',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Artist(models.Model):
    name = models.CharField(
        max_length=222,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ])
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=222,
        null=True,
        blank=True
    )
    bio = models.TextField(
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to=f"artists/",
        null=True,
        blank=True,
    )
    style = models.ForeignKey(Style,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    booking_fee_per_hour = models.PositiveIntegerField(
        verbose_name="Booking Fee per hour",
        null=True,
        blank=True
    )

    class Meta:
        ordering = [
            'name',
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }
        return reverse_lazy('artist page', kwargs)


class Condition(ChoicesEnumMixin, Enum):
    new = 'New'
    very_good_plus = 'Very Good (VG+)'
    very_good = 'Very Good (VG)'
    good_plus = 'Good Plus (G+)'
    mint = 'Mint (M)'
    near_mint = 'Near Mint (NM or M-)'


class Vinyl(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    title = models.CharField(
        max_length=222
    )
    cat_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )
    release_date = models.DateField(
        null=True,
        blank=True
    )
    price = models.FloatField(
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(1000000),
        ],
        null=True,
        blank=True,
        verbose_name='Price ($)'
    )
    record_label = models.ForeignKey(
        RecordLabel,
        on_delete=models.CASCADE,

    )
    cover_art = ImageField(
        upload_to=get_upload_path,
        null=True,
        blank=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    style = ChainedForeignKey(Style,
                              chained_field='genre',
                              chained_model_field='genre',
                              show_all=False,
                              sort=True,
                              null=True,
                              blank=True
                              )
    tracklist = models.TextField(
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        null=True,
        default=1
    )
    condition = models.CharField(
        max_length=123,
        choices=Condition.choices(),
        null=True,
        blank=True
    )
    user = models.ForeignKey(AppUser,
                             on_delete=models.CASCADE,
                             null=True)
    added_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Vinyl'
        verbose_name_plural = 'Vinyl'

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def artist_title(self):
        return f'{self.artist} - {self.title}'


class DJBooking(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)


class VinylPurchase(models.Model):
    # TODO add user
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchased_on = models.DateTimeField(auto_now_add=True)


class Gender(ChoicesEnumMixin, Enum):
    gender = 'Gender'
    do_not_show = 'Do Not Show'
    male = 'Male'
    female = 'Female'


class Profile(models.Model):
    MIN_LEN_FIRST_NAME = 2
    MAX_LEN_FIRST_NAME = 30
    MIN_LEN_LAST_NAME = 2
    MAX_LEN_LAST_NAME = 30
    first_name = models.CharField(
        max_length=MAX_LEN_FIRST_NAME,
        validators=[
            MinLengthValidator(MIN_LEN_FIRST_NAME),
            validate_only_letters,

        ],
        null=True,
    )
    last_name = models.CharField(
        max_length=MAX_LEN_LAST_NAME,
        validators=[MinLengthValidator(MIN_LEN_LAST_NAME), ])
    age = models.PositiveIntegerField(validators=[
        age_validator,
    ],
        null=True,
    )
    gender = models.CharField(
        max_length=Gender.max_len(),
        choices=Gender.choices(),
        null=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Article(models.Model):
    title = models.CharField(
        max_length=100,
    )
    date_added = models.DateField(
    )
    topic = models.ForeignKey(
        Style,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,

    )
    body = models.TextField()
    image = models.ImageField(
        upload_to='articles/',
        null=True,
        blank=True
    )
    headline = models.BooleanField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title
