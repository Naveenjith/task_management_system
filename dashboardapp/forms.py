from django import forms
from taskapp.models import Task, User
from django.contrib.auth.forms import UserCreationForm

class TaskCreationForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        
        if user:
            if user.is_superuser:
                self.fields['assigned_to'].queryset = User.objects.filter(is_superuser=False)
            elif user.groups.filter(name='Admin').exists():
                self.fields['assigned_to'].queryset = User.objects.filter(profile__managed_by=user)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class SuperAdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class UserUpdateForm(forms.ModelForm):
    managed_by = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Admin'),
        required=False,
        label="Managed by (Admin)"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if hasattr(self.instance, 'profile'):
            self.fields['managed_by'].initial = self.instance.profile.managed_by

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
        
        if hasattr(user, 'profile'):
            user.profile.managed_by = self.cleaned_data['managed_by']
            user.profile.save()
        
        return user
        
        
