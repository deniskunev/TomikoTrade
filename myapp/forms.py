from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'phone', 'message', 'privacy_agreed']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'id': 'name-input'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7',
                'id': 'phone-input',
                'pattern': '^\+7\d{10}$'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст сообщения, укажите страну, марку и год машины.',
                'rows': 4,
                'id': 'message-textarea'
            }),
            'privacy_agreed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'privacy-checkbox'
            })
        }
        labels = {
            'name': '',
            'phone': '',
            'message': '',
            'privacy_agreed': ''
        }
        error_messages = {
            'privacy_agreed': {
                'required': 'Необходимо согласиться с политикой конфиденциальности'
            }
        }