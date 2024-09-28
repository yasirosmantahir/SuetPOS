from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url='login')
def dashboard(request):

    user = request.user

    context = {
        'user':user
    }
    return render(request, 'pos/pos.html', context)



class ChangePasswordView(PasswordChangeView):
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('')
