from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from .forms import TaskCreationForm, SuperAdminUserCreationForm, UserUpdateForm
from taskapp.models import Task


# --- Custom Mixins ---
class SuperAdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdminOrSuperAdminMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


# --- Dashboard View ---
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['form'] = kwargs.get('form') or TaskCreationForm(user=user)

        context['is_superadmin'] = user.is_superuser
        context['is_admin'] = user.groups.filter(name='Admin').exists()

        if user.is_superuser:
            all_users = User.objects.prefetch_related('groups').all()
            for u in all_users:
                u.is_admin = u.groups.filter(name='Admin').exists()
            context['all_users'] = all_users
            context['all_tasks'] = Task.objects.all().order_by('-id')

        elif context['is_admin']:
            managed_users = User.objects.filter(profile__managed_by=user)
            context['assigned_tasks'] = Task.objects.filter(assigned_to__in=managed_users).order_by('-id')

        return context


    def post(self, request, *args, **kwargs):
        form = TaskCreationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return self.render_to_response(self.get_context_data(form=form))

# --- User Management Views ---
class UserCreateView(SuperAdminRequiredMixin, CreateView):
    model = User
    form_class = SuperAdminUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('dashboard')


class UserUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('dashboard')


class UserDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('dashboard')


# --- Toggle Admin Status ---
def toggle_admin_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    admin_group, _ = Group.objects.get_or_create(name='Admin')

    if admin_group in user.groups.all():
        user.groups.remove(admin_group)
    else:
        user.groups.add(admin_group)

    return redirect('dashboard')


# --- Task Report Detail ---
class TaskReportDetailView(AdminOrSuperAdminMixin, DetailView):
    model = Task
    template_name = 'task_report.html'
    context_object_name = 'task'
