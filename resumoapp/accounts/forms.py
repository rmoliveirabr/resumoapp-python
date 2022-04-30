from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

from resumoapp.core.utils import generate_hash_key
from resumoapp.core.mail import send_mail_template
from .models import PasswordReset

User = get_user_model()

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário encontrado com este email')

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()

        subject = 'Criar nova senha no Resumo App'
        template_name = 'accounts/password_reset_mail.html'
        context = {'reset': reset}
        send_mail_template(subject, template_name, context, [user.email])

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação de senha não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['name', 'username', 'email']

class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'username', 'email']
