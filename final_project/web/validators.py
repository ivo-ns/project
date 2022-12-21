from django.core import exceptions
from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise exceptions.ValidationError('Only letters are allowed')


def age_validator(value):
    if value < 13:
        raise ValidationError('Age cannot be under 13')
    if value >= 100:
        raise ValidationError('Age cannot be above 100')
