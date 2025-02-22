import random
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View, DetailView, ListView, UpdateView
from apps.forms import VerifyForm, RegistrModelForm
from apps.email import send_email
from apps.models import User, Transaction
from redis import Redis

redis = Redis(decode_responses=True)

class RegisterFormView(FormView):
    template_name = 'app/register.html'
    form_class = RegistrModelForm
    success_url = reverse_lazy('verify_gmail')

    def form_valid(self, form):
        user = form.save()
        email = form.cleaned_data.get('email')
        r_code = random.randrange(10*5, 10*6)
        redis.set(email, r_code)
        redis.expire(email, timedelta(minutes=3))
        send_email(email, r_code)
        self.request.session['email'] = email
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
                # messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class LoginView(View):
    template_name = 'app/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)

        if user.exists():
            user = user.first()
            if check_password(password, user.password):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('profile')
            else:
                messages.error(request, "Email or Password invalid!")
        else:
            messages.error(request, "No account found with this email!")
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class VerifyFormView(FormView):
    template_name = 'app/verify.html'
    form_class = VerifyForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = self.request.session.get('email')
        input_code = form.cleaned_data['code']
        stored_code = redis.get(email)
        if stored_code and str(input_code) == stored_code:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(self.request, "Email muvaffaqiyatli tasdiqlandi!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Kod noto'g'ri yoki muddati o'tgan!")
            return self.form_invalid(form)

class UserProfileListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'app/user_profile.html'
    context_object_name = 'users'
    def get_queryset(self):
        return User.objects.all()
        # return User.objects.order_by('email')

# class UserProfileDetailView(LoginRequiredMixin, DetailView):
#     model = User
#     template_name = 'app/user_profile_edit.html'
#     context_object_name = 'users'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = RegistrModelForm
    template_name = 'app/user_profile_edit.html'
    success_url = reverse_lazy('profile')
    # success_url = reverse_lazy('user_profiles')


    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Profil muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)



class TransactionListView(ListView):
    model = Transaction
    template_name = 'app/transaction.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = self.get_queryset().filter(status='pending').count()
        return context

# class LoginFormView(FormView):
#     template_name = 'app/login.html'
#     success_url = reverse_lazy('verify_gmail')
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)
#
#     def post(self, request, *args, **kwargs):
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user = authenticate(request, email=email, password=password)
#         if user:
#             login(request, user)
#             return redirect(self.success_url)
#         else:
#             messages.error(request, "Username yoki parol noto'g'ri!")
#             return redirect('login')
#
# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('login')