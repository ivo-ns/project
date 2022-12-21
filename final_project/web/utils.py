import os
import string

from django.core.exceptions import ValidationError


def validate_alphabet_characters_english(value):
    for char in value.lower():
        if char.isalpha() and char not in string.ascii_lowercase:
            raise ValidationError('You are not allowed to use non-English characters')


def get_upload_path(instance, filename):
    """ creates unique-Path & filename for upload """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.cat_number, ext)

    return os.path.join(
        instance.record_label.slug, filename
    )
