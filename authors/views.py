from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login,update_session_auth_hash, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post
from . import forms
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.conf import settings
import os
from . models import Profile

def register(request):
    if request.method =='POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account Created Successfully!' )
            return redirect('login')
    else:
        register_form = forms.RegistrationForm()    

    return render(request, 'register_form.html', {'form': register_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_password = form.cleaned_data['password']
            user = authenticate(username = user_name, password = user_password)
            if user is not None:
                messages.success(request, 'Logged in Successfully!' )
                login(request, user)
                return redirect('home')
        else:
            messages.warning(request, 'Login Information is Incorrect' )
            return redirect('register')
    else:
        form = AuthenticationForm()
        return render(request, 'login_form.html', {'form': form, 'type':'Login'})
    
@login_required    
def profile(request):
    data = Post.objects.filter(author = request.user)   

    return render(request, 'profile_form.html', {'data':data}) 
@login_required
def user_update(request):
    if request.method =='POST':
        profile_form = forms.UserUpdateForm(request.POST, instance= request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Account Updated Successfully!' )
            return redirect('profile')
    else:
        profile_form = forms.UserUpdateForm(instance= request.user)    

    return render(request, 'update_profile.html', {'form': profile_form}) 

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Prevents logout after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Replace with your desired URL name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'password_change_form.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')

# class based view
class UserLogin(LoginView):
    template_name = 'login_form.html'
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successfully!')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Your Username or Password is Incorrect!')
        return super().form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('profile')
    
@method_decorator(login_required, name='dispatch')    
class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('profile')  # Replace with your actual URL name

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)  # Prevents logout
        messages.success(self.request, 'Your password was successfully updated!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)   
    
@method_decorator(login_required, name='dispatch')    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.UserUpdateForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('profile')  # Redirect after successful update

    def get_object(self, queryset=None):
        # Always return the current logged-in user
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Account Updated Successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)     
       
# @method_decorator(login_required, name='dispatch')       
# class UserRegisterView(CreateView):
#     form_class = forms.RegistrationForm
#     template_name = 'register_form.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, 'Account Created Successfully!')
#         return response

#     def form_invalid(self, form):
#         messages.error(self.request, 'Please correct the errors below.')
#         return super().form_invalid(form)

class UserRegisterView(CreateView):
    form_class = forms.RegistrationForm
    template_name = 'register_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the user first
        response = super().form_valid(form)

        # Get the uploaded image
        profile_image = form.cleaned_data.get('profile_image')

        if profile_image:
            user = self.object  # newly created user
            # Update or create the associated profile
            Profile.objects.update_or_create(
                user=user,
                defaults={'profile_image': profile_image}
            )

        messages.success(self.request, 'Account Created Successfully!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)              
           