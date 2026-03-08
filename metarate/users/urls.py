from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path, reverse_lazy

from .forms import PasswordChangeFormUser, PasswordResetConfirmForm
from .views import LoginUser, logout_user, RegisterUser, UpdateProfileUser,profile

app_name ='users'

urlpatterns = [
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/',logout_user,name='logout'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('profile/',profile,name='profile'),
    path('update-profile/',UpdateProfileUser.as_view(),name='update_profile'),

    path('password-change/',PasswordChangeView.as_view(
        template_name='universal_form.html',
        extra_context = {'title': "Смена пароля", 'title_button': 'Изменить пароль'},
        form_class=PasswordChangeFormUser,
        success_url = reverse_lazy("users:password_change_done"),
        ),name='password_change'),
    path('password-change-done',PasswordChangeDoneView.as_view(
        template_name = "users/password_change_done.html",
        title='Пароль усмешно изменен!'
    ),name='password_change_done'),


    path('password-reset/',PasswordResetView.as_view(email_template_name = "users/password_reset_email.html",
                                                    template_name='universal_form.html',
                                                    success_url = reverse_lazy("users:password_reset_done"),
                                                    extra_context = {'title': "Восстановление пароля", 'title_button': 'Сбросить по E-mail'}
                                                    ),name='password_reset'),
    path('password-reset/done',PasswordResetDoneView.as_view(
                                    template_name='users/password_reset_done.html'
    ),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="universal_form.html",
                                        success_url = reverse_lazy("users:password_reset_complete"),
                                        form_class=PasswordResetConfirmForm,
                                        extra_context = {'title': "Установите новый пароль", 'title_button': 'Сохранить'}),
         name='password_reset_confirm'
         ),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),


]