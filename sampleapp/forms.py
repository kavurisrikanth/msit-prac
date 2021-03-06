from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(forms.Form):
    username = forms.CharField(label='Choose a username',
                               min_length=3,
                               max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(label='Enter first name',
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name (Optional)'}))
    last_name = forms.CharField(label='Enter last name',
                                max_length=50,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name (Optional)'}))
    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean_username(self):
        uname = self.cleaned_data.get('username').lower()
        qset = User.objects.filter(username=uname)
        if qset.count() > 0:
            raise ValidationError("Username %s is already taken" % uname)
        return uname

    # def clean_email(self):
    #     email = self.cleaned_data.get('email').lower()
    #     qset = User.objects.filter(email=email)
    #     if qset.count() > 0:
    #         raise ValidationError("Account with email address %s exists! Please log in." % email)
    #     return email

    def clean_password2(self):
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError("Passwords do not match.")

        return pwd2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            password=self.cleaned_data.get('password1')
        )
        return user