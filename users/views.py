from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from users.forms import SignUpForm
from users.services.user_services import ProfileService


class SignUp(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': SignUpForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            phone_number = form.cleaned_data.get('phone_number')
            user = authenticate(username=username, password=password)
            ProfileService.profile_create(user=user, number=phone_number)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
