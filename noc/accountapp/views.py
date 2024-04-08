from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
#from .forms import LoginForm



@login_required
def dashboard(request):
    return render(request, 'accountapp/dashboard.html')

class LoginUser(LoginView):
#    form_class = LoginForm
    form_class = AuthenticationForm
    template_name = 'accountapp/login.html'
    extra_context = {'title': 'Авторизация'}

    def form_valid(self, form):
        # Вызов родительского метода для обработки успешной авторизации
        response = super().form_valid(form)

        # Получите URL, на который нужно перенаправить пользователя
        next_url = self.request.POST.get('next', 'accountapp:dashboard')
        return redirect(next_url)

    # def get_success_url(self):
    #     return reverse_lazy('accountapp:dashboard')

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('accountapp:dashboard'))
#     else:
#         form = LoginForm()
#     return render(request, 'accountapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'accountapp/logout.html')


