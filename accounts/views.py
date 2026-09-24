from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'dashboard/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'شما با موفقیت از سیستم خارج شدید.')
        return redirect('dashboard:login')
    return render(request, 'dashboard/logout.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'خطا در ثبت‌نام. لطفاً مجدداً تلاش کنید.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'dashboard/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'dashboard/profile.html', {'user': request.user})

@login_required
def change_password(request):
    from django.contrib.auth.models import User
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not user.check_password(old_password):
            messages.error(request, 'رمز عبور فعلی اشتباه است.')
            return redirect('dashboard:change_password')
        
        if new_password != confirm_password:
            messages.error(request, 'رمزهای عبور مطابقت ندارند.')
            return redirect('dashboard:change_password')
        
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
        return redirect('dashboard:profile')
    
    return render(request, 'dashboard/change_password.html')
