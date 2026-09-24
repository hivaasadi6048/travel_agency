from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': '0912...'}))
    national_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'کد ملی'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'national_code', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('شماره تلفن فقط باید عددی باشد')
        return phone

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام کاربری', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور', 'class': 'form-control'}))

class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور فعلی'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور جدید'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'}))

    class Meta:
        model = User
        fields = ('new_password',)
