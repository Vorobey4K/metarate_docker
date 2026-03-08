from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator
)

class MyUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def get_error_message(self):
        return 'Пароль не должен совпадать с именем пользователя или email'
class MyMinimumLengthValidator(MinimumLengthValidator):
    def get_error_message(self):
        return 'Пароль должен быть не короче 8 символов'

class MyCommonPasswordValidator(CommonPasswordValidator):
    def get_error_message(self):
        return 'Этот пароль слишком простой'

class MyNumericPasswordValidator(NumericPasswordValidator):
    def get_error_message(self):
        return 'Пароль не может состоять только из цифр'