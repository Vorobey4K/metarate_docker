from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.db.models import CharField
from django import forms
from django.forms.widgets import PasswordInput, ClearableFileInput

from .models import Profile
class LoginFormUser(AuthenticationForm):
    username = forms.CharField(label='Логин/E-mail',max_length=40)
    password = forms.CharField(label='Пароль',max_length=40,widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Неверный логин или пароль',
        'inactive': 'Аккаунт неактивен',
    }

class RegisterFormUser(UserCreationForm):
    username = forms.CharField(label='Логин',max_length=40)
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)



    class Meta:
        model = get_user_model()
        fields = ['username','email','password1','password2']
        labels = {'email':'E-mail'}

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Этот логин недоступен')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким e-mail уже существует'
            )
        return email


class UpdateProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', max_length=40)
    email = forms.EmailField(disabled=True, label='E-mail',required=False)
    first_name = forms.CharField(label='Имя', max_length=40,required=False)
    last_name = forms.CharField(label='Фамилия', max_length=40,required=False)
    date_of_birth = forms.DateField(
        required=False,
        label='Дата рождения',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Profile
        fields = ['username','email','first_name','last_name','date_of_birth','photo']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        user = self.instance.user
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name



    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if any([num in name for num in '0123456789']):
            raise forms.ValidationError('Имя может содержать только буквы')
        return name

    def clean_last_name(self):
        name = self.cleaned_data['last_name']
        if any([num in name for num in '0123456789']):
            raise forms.ValidationError('Фамилия может содержать только буквы')
        return name



class PasswordChangeFormUser(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',max_length=40,widget=PasswordInput)
    new_password1 = forms.CharField(label='Новый пароль',max_length=40,widget=PasswordInput)
    new_password2 = forms.CharField(label='Подтверждение пароля',max_length=40,widget=PasswordInput)
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": (
            "Текущий пароль указан неверно"
        ),
        "password_mismatch": (
            'Новые пароли не совпадают'
        )
    }

class PasswordResetConfirmForm(SetPasswordForm):
    new_password1= forms.CharField(label='Новый пароль',max_length=40,widget=PasswordInput)
    new_password2 =  forms.CharField(label='Повтор нового пароля',max_length=40,widget=PasswordInput)


