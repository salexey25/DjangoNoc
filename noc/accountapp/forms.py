from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


# Эта форма будет использована для аутентификации пользователей через базу данных./
# Графический элемент PasswordInput используется для отрисовки /
# HTML-элемента input, включая атрибут type="password"
# class LoginForm(AuthenticationForm):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     # class Meta:
#     #     model = get_user_model()
#     #     fields = ['username', 'password']