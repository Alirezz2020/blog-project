from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.views.generic import DetailView, UpdateView
from .forms import UserRegisterForm, UserLoginForm, CustomPasswordChangeForm, ProfileForm
from blog.models import Post


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                    login(request, user)
                    messages.success(request, 'You are now logged in', 'success')
                    if self.next:
                        return redirect(self.next)
                    return redirect('home:home')
            messages.error(request, 'Invalid username or password', 'error')
        return render(request, self.template_name, {'form': form})
class LogoutView(View):
    def get(self, request):
        return redirect('accounts:logout_confirm')  # Redirect to confirm logout page
class LogoutConfirmView(View):
    def get(self, request):
        return render(request, 'accounts/logout_confirm.html')

    def post(self, request):
        logout(request)
        return redirect('home:home')
class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'registered successfully', 'success')
            return redirect('accounts:login')
        return render(request, self.template_name , {'form': form})
class CustomPasswordChangeView(LoginRequiredMixin, View):
    template_name = 'accounts/password_change_form.html'

    def get(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password1")
            request.user.set_password(new_password)  # Change the password
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in
            messages.success(request, "Your password has been changed successfully!")
            return redirect('password_change_done')  # Redirect to the success page
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {'form': form})
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'
class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')
    email_template_name = 'account/password_reset_email.html'
class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
class ProfileView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Ensure we get the logged-in user's profile
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch posts for the logged-in user
        context['user_posts'] = Post.objects.filter(author=self.request.user)
        return context
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    fields = ['bio', 'profile_picture']
    template_name = 'accounts/profile_update.html'
    success_url = '/accounts/profile/'  # Redirect to profile view after update

    def get_object(self, queryset=None):
        # Ensure that only the logged-in user's profile is updated
        return Profile.objects.get(user=self.request.user)

""" error handling views:"""

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_400(request, exception):
    return render(request, '400.html', status=400)



