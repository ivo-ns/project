from django.contrib.auth import get_user_model, forms as auth_forms
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

from final_project.web.models import Profile, Vinyl, Artist, RecordLabel, Gender, age_validator
from final_project.web.utils import validate_alphabet_characters_english

UserModel = get_user_model()


class SignUpForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(validators=[
        validate_alphabet_characters_english,
        MinLengthValidator(2),
    ])
    last_name = forms.CharField(validators=[
        validate_alphabet_characters_english,
        MinLengthValidator(2),
    ])
    age = forms.IntegerField(validators=[
        age_validator,
    ])
    gender = forms.ChoiceField(
        choices=Gender.choices
    )

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2', 'first_name', 'last_name', 'age', 'gender',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['age'].widget.attrs['placeholder'] = 'Age'
        self.fields['gender'].widget.attrs['placeholder'] = 'Gender'

    # save with data for profile
    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            age=self.cleaned_data['age'],
            gender=self.cleaned_data['gender'],
            user=user,
        )
        if commit:
            profile.save()

        return user


class SignInForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={"autofocus": True, 'placeholder': 'Email...', 'class': "form-control"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'placeholder': 'Password...', 'class': "form-control"}),
    )

    # def __init__(self, *args, **kwargs):
    #     super(SignInForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'


class ArtistAddForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'


class VinylAddForm(forms.ModelForm):
    class Meta:
        model = Vinyl
        exclude = ['user']
        labels = {
            'record_label': 'Record Label',
            'cat_number': 'Catalogue #',
        }
        widgets = {
            'release_date': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

    # artist = AutoCompleteSelectMultipleField('vinyl', required=False, help_text=None)


class LabelAddForm(forms.ModelForm):
    class Meta:
        model = RecordLabel
        fields = '__all__'

        # if UserModel.is_superuser():
        #     fields = '__all__'
        # else:
        #     fields = ('name', 'age', 'location', 'bio')

    # Create empty profile
    # def save(self, commit=True):
    #     user = super().save(commit=commit)
    #     profile = Profile(
    #         user=user,
    #     )
    #     if commit:
    #         profile.save()

#
# class SellForm(forms.ModelForm):
#     class Meta:
#         model = Vinyl
#         fields = '__all__'
#         widgets = {
#             'style': Select(),
#         }
